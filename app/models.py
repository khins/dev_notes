from app.db import get_connection


def add_note(language: str, topic: str, content: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO notes (language, topic, content)
        VALUES (%s, %s, %s)
        """,
        (language, topic, content)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_all_notes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, language, topic FROM notes ORDER BY id")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def get_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row


def update_note(note_id: int, content: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE notes SET content = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (content, note_id)
    )

    conn.commit()
    cur.close()
    conn.close()