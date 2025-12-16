import os

from sqlalchemy import create_engine, text

u = os.getenv("DATABASEURL")
print("DB=", u)

# sync engine for debugging (psycopg)
u2 = u.replace("postgresql+asyncpg", "postgresql")
e = create_engine(u2)

q = """
select d.id, d.root_domain, u.url, u.comment, u.created_at
from blacklist_domains d
left join blacklist_domain_urls u on u.domain_id = d.id
where d.root_domain = 'pulscen.ru'
order by u.id desc
"""
with e.connect() as c:
    print(c.execute(text(q)).fetchall())
