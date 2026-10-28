import pandas as pd
from database import get_connection

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

with get_connection() as conn:
    print("=== applications ===")
    print(pd.read_sql_query("SELECT * FROM applications", conn))

    print("\n=== application_events ===")
    print(pd.read_sql_query("SELECT * FROM application_events", conn))