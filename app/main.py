from app.menu import show_menu, handle_choice


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")
        handle_choice(choice)


if __name__ == "__main__":
    main()