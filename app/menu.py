from app.models import add_note
from app.models import (
    add_note_with_topics,
    get_all_notes,
    get_note_with_topics,
    update_note,
    display_note
)

def show_menu():
    print("\n=== Dev Notes CLI ===")
    print("1. Add Note")
    print("2. View All Notes")
    print("3. View Note by ID")
    print("4. Update Note")
    print("5. Exit")


def handle_choice(choice: str):
    if choice == "1":
        language = input("Language: ")
        title = input("Title: ")

        print("Enter content (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        content = "\n".join(lines)

        topics_input = input("Topics (comma separated): ")

        if topics_input.strip():
            topics = [t.strip().lower() for t in topics_input.split(",") if t.strip()]
        else:
            topics = []

        note_id = add_note_with_topics(language, title, content, topics)

        print(f"✅ Note added with ID {note_id}")

    elif choice == "2":
        notes = get_all_notes()
        for n in notes:
            print(n)

    elif choice == "3":
        note_id = int(input("Enter note ID: "))
        note = get_note_with_topics(note_id)
        display_note(note)

    elif choice == "4":
        note_id = int(input("Enter note ID: "))
        content = input("New content: ")
        update_note(note_id, content)
        print("✏️ Note updated.")

    elif choice == "5":
        print("Goodbye 👋")
        exit()

    else:
        print("Invalid choice.")