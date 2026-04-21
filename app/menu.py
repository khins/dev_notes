import os

from app.models import (
    add_note_with_topics,
    delete_note,
    get_all_languages,
    get_all_notes,
    get_all_topics,
    get_note_with_topics,
    update_note,
    display_note
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    print("\n=== Dev Notes CLI ===")
    print("1. Add Note")
    print("2. View All Notes")
    print("3. View Note by ID")
    print("4. Update Note")
    print("5. Delete Note by ID")
    print("6. Clear Screen")
    print("7. Exit")


def prompt_for_language_selection():
    languages = get_all_languages()

    if not languages:
        print("No saved languages are available yet. Add languages to the database first.")
        return None

    print("\nAvailable languages:")
    for index, (_, name) in enumerate(languages, start=1):
        print(f"{index}. {name}")

    while True:
        selection = input("Select a language number: ").strip()

        try:
            language_index = int(selection)
            if language_index < 1 or language_index > len(languages):
                raise ValueError
        except ValueError:
            print("Invalid selection. Please enter one number from the list.")
            continue

        return languages[language_index - 1][0]


def prompt_for_topic_selection():
    topics = get_all_topics()

    if not topics:
        print("No saved topics are available yet. This note will be added without linked topics.")
        return []

    print("\nAvailable topics:")
    for index, (_, name) in enumerate(topics, start=1):
        print(f"{index}. {name}")

    while True:
        selection = input("Select topic numbers (comma separated), or press Enter for none: ").strip()

        if not selection:
            return []

        try:
            selected_indexes = []
            for part in selection.split(","):
                topic_index = int(part.strip())
                if topic_index < 1 or topic_index > len(topics):
                    raise ValueError
                selected_indexes.append(topic_index)
        except ValueError:
            print("Invalid selection. Please enter only numbers from the list, separated by commas.")
            continue

        unique_indexes = []
        for topic_index in selected_indexes:
            if topic_index not in unique_indexes:
                unique_indexes.append(topic_index)

        return [topics[index - 1][1] for index in unique_indexes]


def handle_choice(choice: str):
    if choice == "1":
        language = prompt_for_language_selection()
        if language is None:
            return

        title = input("Title: ")

        print("Enter content (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        content = "\n".join(lines)

        topics = prompt_for_topic_selection()

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
        print("Enter new content (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        content = "\n".join(lines)
        update_note(note_id, content)
        print("✏️ Note updated.")

    elif choice == "5":
        note_id = int(input("Enter note ID to delete: "))
        deleted = delete_note(note_id)

        if deleted:
            print(f"🗑️ Note {note_id} deleted.")
        else:
            print("❌ Note not found.")

    elif choice == "6":
        clear_screen()

    elif choice == "7":
        print("Goodbye 👋")
        exit()

    else:
        print("Invalid choice.")
