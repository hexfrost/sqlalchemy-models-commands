from asyncpg import connect


async def insert_to_table(conn: connect, table: str, data: dict):
    keys = ", ".join(data.keys())
    nums = ", ".join([f"${num}" for num in range(1, len(data.items()) + 1)])
    values = list(data.values())
    query = f"INSERT INTO {table} ({keys}) VALUES ({nums}) ON CONFLICT DO NOTHING;"
    await conn.execute(query, *values)

