import pandas as pd
from database import get_connection

with get_connection() as conn:
    total = pd.read_sql_query("SELECT COUNT(*) AS n FROM applications", conn)

    ever_interview = pd.read_sql_query(
        """SELECT COUNT(DISTINCT application_id) AS n
           FROM application_events WHERE status = 'Interview'""", conn)

    by_source = pd.read_sql_query(
        """SELECT a.source,
                  COUNT(DISTINCT a.id) AS applications,
                  COUNT(DISTINCT CASE WHEN e.status = 'Interview'
                        THEN a.id END) AS interviews
           FROM applications a
           JOIN application_events e ON e.application_id = a.id
           GROUP BY a.source""", conn)

print(total, ever_interview, by_source, sep="\n\n")