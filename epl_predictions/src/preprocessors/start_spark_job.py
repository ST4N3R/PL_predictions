import pyspark.sql.functions as F
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StringType
from ..utils.setup_logging import setup_logging


class StartSparkJob:
    def __init__(self):
        self.spark = SparkSession.builder.appName("epl").getOrCreate()


    def get_spark_session(self):
        return self.spark