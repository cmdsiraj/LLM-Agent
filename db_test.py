# mysql://<username>:<password>@<host>:<port>/<database>
import pymysql
from collections import defaultdict

connection  = pymysql.connect(
    host="localhost",
    password="password",
    user="root",
    port=3306,
    database="sakila"
)


with connection.cursor() as cursor:
    query = (
    "SELECT table_name, column_name, data_type, is_nullable, column_key, column_default, extra "
    "FROM information_schema.columns "
    "WHERE table_schema='sakila' "
    "ORDER BY table_name, ordinal_position;"
    )
    cursor.execute(query=query)
    columns = cursor.fetchall()

with connection.cursor() as cursor:
    query = (
        "SELECT table_name, column_name, referenced_table_name, referenced_column_name "
        "FROM information_schema.key_column_usage "
        "WHERE referenced_table_name IS NOT NULL "
        "AND table_schema='sakila'"
    )

    cursor.execute(query)
    foreign_keys = cursor.fetchall()

schema = defaultdict(list)

for table, column, data_type, is_nullable, column_key, column_default, extra in columns:
    schema[table].append({
        "column": column,
        "data_type": data_type,
        "is_nullable":is_nullable,
        "column_key": column_key,
        "column_default": column_default,
        "extra": extra
    })

foreign_map = defaultdict(list)

for table, column, ref_table, ref_col in foreign_keys:
    foreign_map[table].append({
        "column": column,
        "references": f"{ref_table}({ref_col})"
    })