from db import get_connection, init_db

ORGANISERS = [
    ("drippedparty", "https://linktr.ee/drippedparty"),
    ("chocolatecity", "https://linktr.ee/chocolatecity"),
    ("yusu.coffee", "https://linktr.ee/yusu.coffee"),
    ("striptopia", "https://linktr.ee/striptopia"),
    ("mosaikomagazine", "https://linktr.ee/mosaikomagazine")
]


def seed():
    with get_connection() as conn:
        init_db(conn)
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT INTO organisers (name, profile_url) VALUES (%s, %s)
            ON CONFLICT (profile_url) DO NOTHING;""",
            ORGANISERS,
        )
    print(f"Seeded {len(ORGANISERS)} organisers.")


if __name__ == "__main__":
    seed()
