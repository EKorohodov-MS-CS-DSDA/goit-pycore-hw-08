from functools import wraps
from typing import Callable
from address_book import AddressBook
from record import Record
from serialization import save_data, load_data


def input_error(func: Callable) -> Callable:
    """
    A decorator wrapper to handle input errors in the given function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"[{func.__name__}] {e}"
        except IndexError as e:
            return f"[{func.__name__}] {e}"
        except KeyError as e:
            return f"[{func.__name__}] {e}"
    return wrapper

@input_error
def add_contact(args: list, address_book: AddressBook) -> str:
    """
    Add a new contact to the address book, or adds a phone number to an existing contact.
    Parameters:
        args (list): A list of strings representing the contact information.
            The elements are: name, phone.
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string indicating the result of the operation.
    Raises:
        ValueError: If the number of args is less than 2.
    """
    if len(args) < 2:
        raise ValueError("Not enough arguments. Input: add <name> <phone>")

    data = {"name": ' '.join(args[:-1]), "phone": args[-1]}
    record = address_book.find(data["name"])
    if record is None:
        record = Record(data["name"])
        address_book.add_record(record)
    if data["phone"]:
        record.add_phone(data["phone"])

    return f"Added {data['name']} with phone {data['phone']}"


@input_error
def change_contact(args: list, address_book: AddressBook) -> str:
    """
    Change the phone number associated with a given name in the given contacts dictionary.
    Parameters:
        args (list): A list of strings representing the name of the contact and 
            the new phone number.
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string indicating the result of the operation.
    Raises:
        ValueError: If the number of args is less than 3 or if the name is not found in 
            the contacts dictionary.
    """
    if len(args) < 3:
        raise ValueError("Not enough arguments. Input: change <name> <old phone> <new phone>")

    data = {"name": ' '.join(args[:len(args) - 2]), "old_phone": args[-2], "new_phone": args[-1]}

    record = address_book.find(data["name"])
    if record is None:
        raise ValueError(f"Can't find {data['name']} name")
    else:
        record.edit_phone(data["old_phone"], data["new_phone"])

    return f"Updated {data['name']} with new phone {data['new_phone']}"


@input_error
def show_phone(args: list, address_book: AddressBook) -> str:
    """
    Returns the phone numbers associated with a given name in the given contacts dictionary.
    Parameters:
        args (list): A list of strings representing the name of the contact.
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string containing the phone numbers associated with the given name.
    Raises:
        ValueError: If the number of args is less than 1 or if the name is not found in
    """
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: phone <name>")

    name = ' '.join(args)
    record = address_book.find(name)
    if record is not None:
        return record

    return f"Can't find {name} name"


@input_error
def show_all(address_book: AddressBook) -> str:
    """
    Returns a string containing all the contacts in the AddressBook.
    Parameters:
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string containing all the contacts in the AddressBook.
    """
    if address_book.data:
        return address_book
    else:
        return "No contacts"


@input_error
def add_birthday(args, address_book: AddressBook) -> str:
    """
    Add the birthday information to the record.
    Parameters:
        args (list): A list of strings representing the name of the contact and
            the birthday.
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string indicating the result of the operation.
    Raises:
        ValueError: If the number of args is less than 2 or if the name is not found in
            the contacts dictionary.
    """
    if len(args) < 2:
        raise ValueError("Not enough arguments. Input: add-birthday <name> <birthday>")

    data = {"name": ' '.join(args[:-1]), "birthday": args[-1]}
    record = address_book.find(data["name"])
    if record is None:
        return f"Can't find {data['name']} name"

    record.add_birthday(data["birthday"])
    return f"Birthday added for {data['name']}"


@input_error
def show_birthday(args, address_book: AddressBook) -> str:
    """
    Returns the birthday associated with a given name in the AddressBook.
    Parameters:
        args (list): A list of strings representing the name of the contact.
        address_book (AddressBook): An instance of the AddressBook class.
    Returns:
        str: A string containing the birthday associated with the given name.
    Raises:
        ValueError: If the number of args is less than 1 or if the name is not found in
    """
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: show-birthday <name>")

    name = ' '.join(args)
    record = address_book.find(name)
    if record is not None:
        return f"{name} birthday is {record.birthday}"
    return f"Can't find {name} name"


@input_error
def birthdays(args, address_book: AddressBook) -> list:
    """
    Returns the upcoming birthdays.
    Parameters: Currently unused
    """
    return address_book.get_upcoming_birthdays()


def parse_input(input_str: str) -> tuple:
    command, *args = input_str.split()
    command = command.strip().lower()
    return command, *args


def main():
    address_book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        input_str = input("Enter command: ")
        command, *args = parse_input(input_str)

        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, address_book))
            case "change":
                print(change_contact(args, address_book))
            case "phone":
                print(show_phone(args, address_book))
            case "all":
                print(show_all(address_book))
            case "add-birthday":
                print(add_birthday(args, address_book))
            case "show-birthday":
                print(show_birthday(args, address_book))
            case "birthdays":
                print(birthdays(args, address_book))
            case "exit" | "quit":
                break
            case _:
                print("Invalid command.")

    save_data(address_book)
    print("Good bye!")


if __name__ == "__main__":
    main()
