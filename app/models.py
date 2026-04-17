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

def get_or_create_topic(name: str) -> int:
    conn = get_connection()
    cur = conn.cursor()

    # Try to get existing topic
    cur.execute("SELECT id FROM topics WHERE name = %s", (name,))
    row = cur.fetchone()

    if row:
        topic_id = row[0]
    else:
        cur.execute(
            "INSERT INTO topics (name) VALUES (%s) RETURNING id",
            (name,)
        )
        topic_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return topic_id

def link_note_topic(note_id: int, topic_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO note_topics (note_id, topic_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (note_id, topic_id)
    )

    conn.commit()
    cur.close()
    conn.close()

def add_note_with_topics(language: str, title: str, content: str, topics: list[str]):
    note_id = add_note(language, title, content)

    for topic in topics:
        topic_clean = topic.strip().lower()
        topic_id = get_or_create_topic(topic_clean)
        link_note_topic(note_id, topic_id)

    return note_id