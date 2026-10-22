from database.init_db import connect, init_db


def test_init_db_removes_legacy_category_column(tmp_path):
    path = tmp_path / "legacy.db"
    conn = connect(str(path))
    conn.execute(
        "CREATE TABLE items ("
        "id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, description TEXT, "
        "category TEXT NOT NULL CHECK (category IN ('electronics', 'other')), "
        "item_type TEXT, location TEXT, item_date DATE, image_url TEXT, "
        "contact_email TEXT, status TEXT, created_at TIMESTAMP, updated_at TIMESTAMP)"
    )
    conn.execute(
        "INSERT INTO items (id, title, description, category) VALUES (1, 'Old item', 'Existing report', 'other')"
    )

    init_db(conn)

    columns = {row["name"] for row in conn.execute("PRAGMA table_info(items)")}
    row = conn.execute("SELECT id, title FROM items WHERE id = 1").fetchone()
    conn.close()

    assert "category" not in columns
    assert row["title"] == "Old item"
