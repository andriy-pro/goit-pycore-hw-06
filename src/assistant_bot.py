import sys

from typing import Callable, Dict, List, Optional
from collections import UserDict
from colorama import Fore, Style, init


class Field:
    """Base class for all fields in a record.

    Parameters
    ----------
    value : str
        The value of the field.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        """Return the string representation of the field.

        Returns
        -------
        str
            The string representation of the field value.
        """
        return str(self.value)


class Name(Field):
    """Class for storing contact names. Inherits from Field.

    Parameters
    ----------
    value : str
        The name of the contact.

    Raises
    ------
    ValueError
        If the name is empty.
    """

    def __init__(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    """Class for storing phone numbers. Inherits from Field.

    Parameters
    ----------
    value : str
        The phone number.

    Raises
    ------
    ValueError
        If the phone number is not 10 digits long.
    """

    def __init__(self, value: str):
        if not value.isdigit() or len(value.strip()) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Record:
    """Class for storing contact information, including name and phone numbers.

    Parameters
    ----------
    name : Name
        The name of the contact.
    """

    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: Phone):
        """Add a phone number to the contact.

        Parameters
        ----------
        phone : Phone
            The phone number to add.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: Phone):
        """Remove a phone number from the contact.

        Parameters
        ----------
        phone : Phone
            The phone number to remove.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Edit an existing phone number in the contact.

        Parameters
        ----------
        old_phone : Phone
            The old phone number to be replaced.
        new_phone : Phone
            The new phone number to replace with.
        """
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: Phone):
        """Find a phone number in the contact.

        Parameters
        ----------
        phone : Phone
            The phone number to find.

        Returns
        -------
        Phone or None
            The found phone number object, or None if not found.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        """Return the string representation of the contact.

        Returns
        -------
        str
            The string representation of the contact.
        """
        phones = "; ".join([str(phone) for phone in self.phones])
        return f"Contact name: {self.name}, phones: {phones}"


class AddressBook(UserDict):
    """Class for storing and managing contact records.

    Inherits from UserDict.
    """

    def add_record(self, record: Record):
        """Add a record to the address book.

        Parameters
        ----------
        record : Record
            The record to add.
        """
        self.data[record.name.value] = record

    def delete(self, name: Name):
        """Delete a record from the address book by name.

        Parameters
        ----------
        name : Name
            The name of the contact to delete.

        Raises
        ------
        KeyError
            If the record with the given name is not found.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name '{name}' not found")

    def find(self, name: Name) -> Record:
        """Find a record in the address book by name.

        Parameters
        ----------
        name : Name
            The name of the contact to find.

        Returns
        -------
        Record or None
            The found record object, or None if not found.
        """
        return self.data.get(name, None)

    def __str__(self):
        """Return the string representation of the address book.

        Returns
        -------
        str
            The string representation of all records in the address book.
        """
        return "\n".join(str(record) for record in self.data.values())


def input_error(handler: Callable) -> Callable:
    """Decorator for handling errors in command functions."""

    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except TypeError as e:
            print(
                f"{Fore.RED}Error: Incorrect command.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
            help_command()
        except ValueError as e:
            print(
                f"{Fore.RED}Error: Incorrect arguments.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except KeyError as e:
            print(
                f"{Fore.RED}Error: Contact not found.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except IndexError as e:
            print(
                f"{Fore.RED}Error: Index out of range.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except Exception as e:
            print(
                f"{Fore.RED}An unexpected error occurred:\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )

    return wrapper


def parse_input(user_input: str) -> tuple[str, List[str]]:
    """Parse the user input into a command and arguments.

    Parameters
    ----------
    user_input : str
        The input string from the user.

    Returns
    -------
    tuple[str, List[str]]
        The command and a list of arguments.
    """
    parts = user_input.lower().split()
    command = parts[0] if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args


@input_error
def handle_command(
    command_handlers: Dict[str, Callable[[Optional[List[str]]], None]],
    command: str,
    args: Optional[List[str]],
) -> None:
    """Handle the given command using the appropriate handler.

    Parameters
    ----------
    command_handlers : Dict[str, Callable[[Optional[List[str]]], None]]
        A dictionary mapping commands to their handlers.
    command : str
        The command to handle.
    args : Optional[List[str]]
        The arguments for the command.
    """
    if command in command_handlers:
        if args is None:
            args = []  # Use an empty list if no arguments are provided
        command_handlers[command](args)
    else:
        raise TypeError(f"Unknown command '{command}'")


@input_error
def hello() -> None:
    """Greet the user."""
    print(f"{Fore.CYAN}How can I help you?{Style.RESET_ALL}")


@input_error
def add_contact(contacts: Dict[str, str], *args: str) -> None:
    """Add a new contact.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name and phone number of the new contact.
    """
    if len(args) != 2:
        raise ValueError("Usage: add [name] [phone number]")
    name, phone = args
    if name in contacts:
        if contacts[name] == phone:
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" with phone number "{Fore.CYAN}{phone}{Fore.YELLOW}" already exists.{Style.RESET_ALL}'
            )
        else:
            current_phone = contacts[name]
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" is already added with the number "{Fore.CYAN}{current_phone}{Fore.YELLOW}".\nTo change the number, use the "{Style.RESET_ALL}change{Fore.YELLOW}" command.{Style.RESET_ALL}'
            )
    else:
        contacts[name] = phone
        print(
            f'{Fore.GREEN}Contact "{Fore.CYAN}{name}{Fore.GREEN}" added with phone number "{Fore.CYAN}{phone}{Fore.GREEN}".{Style.RESET_ALL}'
        )


@input_error
def change_contact(contacts: Dict[str, str], *args: str) -> None:
    """Change an existing contact's phone number.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name and new phone number of the contact.
    """
    if len(args) != 2:
        raise ValueError("Usage: change [name] [new phone number]")
    name, new_phone = args
    if name in contacts:
        current_phone = contacts[name]
        if new_phone == current_phone:
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" already has this phone number: "{Fore.CYAN}{new_phone}{Fore.YELLOW}". No changes were made.{Style.RESET_ALL}'
            )
        else:
            contacts[name] = new_phone
            print(
                f'{Fore.GREEN}For user {Fore.CYAN}"{name}"{Fore.GREEN}, the phone has been changed from "{Fore.CYAN}{current_phone}{Fore.GREEN}" to "{Fore.CYAN}{new_phone}{Fore.GREEN}".{Style.RESET_ALL}'
            )
    else:
        raise KeyError(f"Name '{name}' not found.")


@input_error
def show_phone(contacts: Dict[str, str], *args: str) -> None:
    """Show the phone number of a contact.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name of the contact.
    """
    if len(args) != 1:
        raise ValueError("Usage: phone [name]")
    name = args[0]
    if name in contacts:
        print(
            f'{Fore.GREEN}Phone number of "{Fore.CYAN}{name}{Fore.GREEN}": {Fore.CYAN}{contacts[name]}{Style.RESET_ALL}'
        )
    else:
        raise KeyError(f"Name '{name}' not found.")


@input_error
def show_all_contacts(contacts: Dict[str, str]) -> None:
    """Show all contacts.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    """
    if contacts:
        for name, phone in contacts.items():
            print(f"{Fore.GREEN}{name}: {Fore.CYAN}{phone}{Style.RESET_ALL}")
    else:
        raise IndexError("No contacts available.")


def handle_exit() -> None:
    """Exit the program."""
    print(f"{Fore.GREEN}{Style.BRIGHT}Good bye!{Style.RESET_ALL}")
    sys.exit()


def help_command():
    """Display the help information with available commands."""
    print(f"{Fore.GREEN}This bot helps you manage your contacts.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}You can use the following commands:{Style.RESET_ALL}")
    print(f"hello{Fore.GREEN} - Greets the user.{Style.RESET_ALL}")
    print(
        f"add [name] [phone number]{Fore.GREEN} - Adds a new contact.{Style.RESET_ALL}"
    )
    print(
        f"change [name] [new phone number]{Fore.GREEN} - Changes the phone number of an existing contact.{Style.RESET_ALL}"
    )
    print(
        f"phone [name]{Fore.GREEN} - Shows the phone number of a contact.{Style.RESET_ALL}"
    )
    print(f"all{Fore.GREEN} - Shows all contacts.{Style.RESET_ALL}")
    print(f"close, exit, quit{Fore.GREEN} - Exits the program.{Style.RESET_ALL}")
    print(f"help{Fore.GREEN} - Displays a list of available commands.{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Example usage:{Style.RESET_ALL}")
    print(
        f"add John 1234567890{Fore.GREEN} - Adds a contact named {Fore.CYAN}John{Fore.GREEN} with phone number {Fore.CYAN}1234567890.{Style.RESET_ALL}"
    )
    print(
        f"phone John{Fore.GREEN} - Shows the phone number of {Fore.CYAN}John.{Style.RESET_ALL}\n"
    )


def main():
    """Main function that runs the command line interface for an assistant bot."""
    contacts: Dict[str, str] = {}
    command_handlers: Dict[str, Callable[[Optional[List[str]]], None]] = {
        "hello": lambda _: hello(),
        "add": lambda args: add_contact(contacts, *args),
        "change": lambda args: change_contact(contacts, *args),
        "phone": lambda args: show_phone(contacts, *args),
        "all": lambda _: show_all_contacts(contacts),
        "close": lambda _: handle_exit(),
        "exit": lambda _: handle_exit(),
        "quit": lambda _: handle_exit(),
        "help": lambda _: help_command(),
    }

    init(autoreset=True)  # Initialize colorama

    banner_part_1 = """
     _               _       _                 _     ____          _                ____  
    / \    ___  ___ (_) ___ | |_  __ _  _ __  | |_  | __ )   ___  | |_    __   __  |___ \ 
   / _ \  / __|/ __|| |/ __|| __|/ _` || '_ \ | __| |  _ \  / _ \ | __|   \ \ / /    __) |
  / ___ \ \__ \\\__ \| |\__ \| |_| (_| || | | || |_  | |_) || (_) || |_     \ V /_   / __/ 
 /_/   \_\|___/|___/|_||___/ \__|\__,_||_| |_| \__| |____/  \___/  \__|     \_/(_) |_____|
                                                                                          
"""
    print(f"{Fore.GREEN}{banner_part_1}{Style.RESET_ALL}")
    print()
    print(
        f"{Fore.CYAN}{Style.BRIGHT}Welcome to the Assistant Bot ver. 2.1 !{Style.RESET_ALL}"
    )
    print()
    help_command()

    while True:
        user_input = input(f"{Fore.YELLOW}Enter a command: {Style.RESET_ALL}").strip()
        command, args = parse_input(user_input)
        handle_command(command_handlers, command, args)


if __name__ == "__main__":
    main()
