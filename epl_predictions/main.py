from src.data.table_scrapper import TableScrapper


currtable = TableScrapper()
# curr_df = currtable.get_current_table()
# currtable.save_table(curr_df, "current_table")

prev_df = currtable.get_previous_tables()
currtable.save_table(prev_df, "previous_tables")