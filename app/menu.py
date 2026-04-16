from app.models import add_note, get_all_notes, get_note, update_note


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
        topic = input("Topic: ")
        content = input("Content: ")

        add_note(language, topic, content)
        print("✅ Note added.")

    elif choice == "2":
        notes = get_all_notes()
        for n in notes:
            print(n)

    elif choice == "3":
        note_id = int(input("Enter note ID: "))
        note = get_note(note_id)
        print(note)

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