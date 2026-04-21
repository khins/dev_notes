from app.db import get_connection


def add_note(language_id: int, title: str, content: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO notes (language_id, title, content)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (language_id, title, content)
    )
    note_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return note_id


def get_all_notes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT n.id, l.name, n.title
        FROM notes n
        JOIN languages l ON l.id = n.language_id
        ORDER BY n.id
        """
    )
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


def delete_note(note_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
    deleted_row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    return deleted_row is not None


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


def get_all_languages():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM languages ORDER BY name")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def get_all_topics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM topics ORDER BY name")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

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

def add_note_with_topics(language_id: int, title: str, content: str, topics: list[str]):
    note_id = add_note(language_id, title, content)

    for topic in topics:
        topic_clean = topic.strip().lower()
        topic_id = get_or_create_topic(topic_clean)
        link_note_topic(note_id, topic_id)

    return note_id

def get_note_with_topics(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT n.id, l.name, n.title, n.content,
               STRING_AGG(t.name, ', ') as topics
        FROM notes n
        JOIN languages l ON l.id = n.language_id
        LEFT JOIN note_topics nt ON n.id = nt.note_id
        LEFT JOIN topics t ON t.id = nt.topic_id
        WHERE n.id = %s
        GROUP BY n.id, l.name
        """,
        (note_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()
    return row

def display_note(note):
    if not note:
        print("❌ Note not found")
        return

    note_id, language, title, content, topics = note

    print("\n" + "="*30)
    print(f"ID: {note_id}")
    print(f"Language: {language}")
    print(f"Title: {title}")

    print("\nContent:")
    print(content)  # 👈 this preserves line breaks!

    print("\nTopics:", topics if topics else "None")
    print("="*30 + "\n")
