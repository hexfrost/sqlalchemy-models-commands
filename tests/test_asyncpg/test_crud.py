import os

import psycopg2
import pytest

from asyncpg import connect
from dotenv import load_dotenv

load_dotenv()

from simplecrud import insert_to_table


@pytest.fixture(autouse=True)
def database_url():
    return os.getenv("TEST_DATABASE_URL")

@pytest.fixture(autouse=True)
def table():
    with psycopg2.connect(os.getenv("TEST_DATABASE_URL")) as pg_conn:
        cur = pg_conn.cursor()
        table = "test_table"
        cur.execute(f"CREATE TABLE {table} (id SERIAL PRIMARY KEY, name TEXT, age INT)")
        pg_conn.commit()
        yield table
        cur.execute(f"DROP TABLE {table}")
        pg_conn.commit()


@pytest.mark.asyncio
async def test_insert_to_table(database_url):
    data = {"name": "test", "age": 20}
    table = "test_table"
    conn = await connect(dsn=database_url)
    await insert_to_table(conn, table, data)
    with psycopg2.connect(database_url) as pg_conn:
        cur = pg_conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        result = cur.fetchall()
        assert result == [(1, "test", 20)]
