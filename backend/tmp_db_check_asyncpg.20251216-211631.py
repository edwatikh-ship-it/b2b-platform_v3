import asyncio
import os

import asyncpg

SQL = """
select d.id, d.root_domain, u.url, u.comment, u.created_at
from blacklist_domains d
left join blacklist_domain_urls u on u.domain_id = d.id
where d.root_domain = 'pulscen.ru'
order by u.id desc
"""


def to_pg_dsn(dsn: str) -> str:
    # asyncpg понимает postgresql://, а не postgresql+asyncpg://
    if dsn.startswith("postgresql+asyncpg://"):
        return "postgresql://" + dsn[len("postgresql+asyncpg://") :]
    return dsn


async def main():
    dsn = os.getenv("DATABASEURL")
    print("DATABASEURL=", dsn)
    pg_dsn = to_pg_dsn(dsn)
    conn = await asyncpg.connect(pg_dsn)
    try:
        rows = await conn.fetch(SQL)
        print(list(rows))
    finally:
        await conn.close()


asyncio.run(main())
