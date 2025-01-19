import pyspark.sql.functions as F
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from ..utils.setup_logging import setup_logging
from .start_spark_job import StartSparkJob


class ProcessLeagueTable:
    def __init__(self):
        spark_job = StartSparkJob()
        self.spark = spark_job.get_spark_session()

        self.logger = setup_logging()
        

    def _change_column_types(self, df: SparkDataFrame) -> SparkDataFrame:
        columns_to_cast_int = ["MP", "W", "D", "L", "GD", "Pts", "GF", "GA"]
        columns_to_cast_float = ["Pts/MP", "xG", "xGA", "xGD", "xGD/90"]

        try:
            for column in columns_to_cast_int:
                df = df.withColumn(column, F.col(column).cast("integer"))

            for column in columns_to_cast_float:
                df = df.withColumn(column, F.col(column).cast("float"))

            self.logger.debug("Casted columns to proper types")
        except Exception as e:
            self.logger.error(e)
        
        return df
    

    def _remove_unnecessary_columns(self, df: SparkDataFrame) -> SparkDataFrame:
        columns_to_delete = ["Attendance", "Top Team Scorer", "Goalkeeper", "Notes"]
        
        try:
            df = df.drop(*columns_to_delete)
            self.logger.debug("Deleted unnecessary columns")
        except Exception as e:
            self.logger.error(e)
        
        return df


    def _remove_spaces(self, df: SparkDataFrame) -> SparkDataFrame:
        try:
            df = df.withColumn("Last 5", F.regexp_replace(F.col("Last 5"), " ", ""))
            
            self.logger.debug("Deleted spaces from columns")
        except Exception as e:
            self.logger.error(e)
        
        return df
    

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        df = self.spark.createDataFrame(data)

        df = self._change_column_types(df)
        df = self._remove_unnecessary_columns(df)
        df = self._remove_spaces(df)

        pandas_df = df.toPandas()

        return pandas_df