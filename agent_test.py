from MyAgent.Agent.MyAgent import Agent
from MyAgent.Tools.FileReaderTool import FileReaderTool
import json
from MyAgent.Knowledge.KnowledgeSource import FileKnowledge
import pymysql
from dotenv import load_dotenv
import os
from collections import defaultdict
from MyAgent.LLM.GeminiLLM import GeminiLLM
from urllib.parse import urlparse

# mysql://<username>:<password>@<host>:<port>/<database>
def get_schema(conn_string: str):

    parsed = urlparse(conn_string)

    database = parsed.path.lstrip("/")

    connection = pymysql.connect(
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
        database=database
    )

    with connection.cursor() as cursor:
        query = (
        "SELECT table_name, column_name, data_type, is_nullable, column_key, column_default, extra "
        "FROM information_schema.columns "
        f"WHERE table_schema='{database}' "
        "ORDER BY table_name, ordinal_position;"
        )
        cursor.execute(query=query)
        columns = cursor.fetchall()

    with connection.cursor() as cursor:
        query = (
            "SELECT table_name, column_name, referenced_table_name, referenced_column_name "
            "FROM information_schema.key_column_usage "
            "WHERE referenced_table_name IS NOT NULL "
            f"AND table_schema='{database}'"
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
    
    return schema, foreign_map

def main():
    load_dotenv()
    conn_string = os.getenv("DATABASE_STRING")
    schema, foreign_map=get_schema(conn_string=conn_string)

    role = (
        "You are a friendly and knowledgeable SQL assistant who helps users interact with databases through natural language. "
        "You specialize in converting user queries into valid and efficient SQL based on the provided database schema."
    )

    goal = (
        "Your goal is to understand the user's question, analyze the given database schema, and generate accurate SQL queries. "
        "You must ensure that your answers follow proper SQL syntax and reflect the schema structure. "
        "If the user's question is unclear or lacks details, ask clarifying questions. "
        "If no schema is provided or accessible, clearly respond with: 'I cannot answer this without a database schema.' "
        "The schema of the database is in the format { table:{column:data_type} } and the schema is:\n"
        f"{schema}"
        "And also the relation between tables:\n"
        f"{foreign_map}"
        "Do not assume table or column names that are not explicitly part of the schema."
    )

    back_story = (
        "You were created to assist developers, analysts, and business users in querying databases without needing to know SQL. "
        "You've been trained on numerous schemas and SQL examples and understand how to interpret natural language requests into structured queries. "
        "You aim to make querying data simple, accurate, and approachable — like having a smart, supportive teammate always ready to help. "
        "You are careful, transparent, and do not guess. If the information or schema you need is missing, you acknowledge it clearly instead of fabricating a response."
    )

    llm = GeminiLLM(model_name="gemini-2.0-flash-lite")

    model = Agent (
        role=role,
        goal=goal,
        back_story=back_story,
        llm=llm
    )


    while(True):
        print("\n\nEnter '/exit' or '/quit' or '/bye' to quit")
        input_text = input("You: ").strip()

        if input_text.lower() in ['/exit', '/quit', '/bye']:
            break
        
        reply = model.chat(input_text)
        print(f"\nAgent: {reply}")
    
    history = [model.system_prompt]+model.chat_history
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)


main()