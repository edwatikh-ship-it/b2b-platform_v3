import os
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def _print_columns(conn, table: str) -> None:
    r = await conn.execute(
        text(
            "select column_name, data_type "
            "from information_schema.columns "
            "where table_schema='public' and table_name=:t "
            "order by ordinal_position;"
        ),
        {"t": table},
    )
    cols = r.fetchall()
    print(f"{table} columns:", [(c[0], c[1]) for c in cols])


async def main() -> None:
    url = os.getenv("DATABASEURL") or os.getenv("DATABASE_URL")
    print("DB URL set:", bool(url))
    if not url:
        return

    engine = create_async_engine(url, echo=False)
    try:
        async with engine.connect() as c:
            r = await c.execute(
                text(
                    "select tablename "
                    "from pg_tables "
                    "where schemaname='public' "
                    "and tablename ilike '%suppl%';"
                )
            )
            tables = [row[0] for row in r.fetchall()]
            print("Tables:", tables)

            for t in ("suppliers", "supplier_urls"):
                if t in tables:
                    await _print_columns(c, t)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
