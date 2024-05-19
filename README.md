# goit-pycore-hw-06
*Repository for storing solutions to algorithmic homework assignments for GoIT Python Course, Homework 06.*
***

[🇺🇦 *Українська версія*](#uk)
<span id="en"></span>

## Console Assistant Bot: Address Book Management System

### Task

Develop the internal logic of an [**assistant**](https://github.com/andriy-pro/goit-pycore-hw-04?tab=readme-ov-file#task-4) *(["Console Assistant Bot v.2"](https://github.com/andriy-pro/goit-pycore-hw-05?tab=readme-ov-file#task-4))* to work with an address book using object-oriented programming. Implement classes to manage contacts, including data storage and manipulation.

### Entities

- **Field**: base class for record fields.
- **Name**: class for storing the contact's name. Required field.
- **Phone**: class for storing phone numbers. Validates the format (10 digits).
- **Record**: class for storing contact information, including name and a list of phone numbers.
- **AddressBook**: class for storing and managing records.

### Functionality

- **AddressBook**:
  - Add records.
  - Search records by name.
  - Delete records by name.
- **Record**:
  - Add phone numbers.
  - Delete phone numbers.
  - Edit phone numbers.
  - Search phone numbers.

### Recommendations for Implementation

```python
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Implement the Name class
    pass

class Phone(Field):
    # Implement the Phone class
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Implement the Record class

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # Implement the AddressBook class
    pass
```

### Example Execution

```python
# Creating a new address book
book = AddressBook()

# Creating a record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Adding John's record to the address book
book.add_record(john_record)

# Creating and adding a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Displaying all records in the book
for name, record in book.data.items():
    print(record)

# Finding and editing John's phone number
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Output: 'Contact name: John, phones: 1112223333; 5555555555'

# Searching for a specific phone number in John's record
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Output: 'John: 5555555555'

# Deleting Jane's record
book.delete("Jane")
```

### Evaluation Criteria

- **AddressBook**:
  - Implement the `add_record` method to add a record to `self.data`.
  - Implement the `find` method to locate a record by name.
  - Implement the `delete` method to remove a record by name.
- **Record**:
  - Store a `Name` object in a separate attribute.
  - Store a list of `Phone` objects in a separate attribute.
  - Implement methods to add (`add_phone`), delete (`remove_phone`), edit (`edit_phone`), and search for `Phone` objects (`find_phone`).
- **Phone**:
  - Implement phone number validation (check for 10 digits).


***
***

[🇬🇧 *English Version*](#en)
<span id="uk"></span>

## Консольний бот-помічник: Розробка системи управління адресною книгою

### Завдання

Розробити внутрішню логіку [**асистента**](https://github.com/andriy-pro/goit-pycore-hw-04?tab=readme-ov-file#%D0%B7%D0%B0%D0%B2%D0%B4%D0%B0%D0%BD%D0%BD%D1%8F-4) *(["Консольний бот-помічник вер.2"](https://github.com/andriy-pro/goit-pycore-hw-05?tab=readme-ov-file#%D0%B7%D0%B0%D0%B2%D0%B4%D0%B0%D0%BD%D0%BD%D1%8F-4))* для роботи з адресною книгою, використовуючи об'єктно-орієнтоване програмування. Реалізувати класи для роботи з контактами, включаючи зберігання даних та маніпуляції з ними.

### Сутності

- **Field**: базовий клас для полів запису.
- **Name**: клас для зберігання імені контакту. Обов'язкове поле.
- **Phone**: клас для зберігання номера телефону. Має валідацію формату (10 цифр).
- **Record**: клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
- **AddressBook**: клас для зберігання та управління записами.

### Функціональність

- **AddressBook**:
  - Додавати записи.
  - Шукати записи за іменем.
  - Видаляти записи за іменем.
- **Record**:
  - Додавати телефони.
  - Видаляти телефони.
  - Редагувати телефони.
  - Шукати телефони.

### Рекомендації для виконання

```python
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Реалізувати клас Name
    pass

class Phone(Field):
    # Реалізувати клас Phone
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Реалізувати клас Record

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # Реалізувати клас AddressBook
    pass
```

### Приклад виконання

```python
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: 'Contact name: John, phones: 1112223333; 5555555555'

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 'John: 5555555555'

# Видалення запису Jane
book.delete("Jane")
```

### Критерії оцінювання

- **AddressBook**:
  - Реалізовано метод `add_record`, який додає запис до `self.data`.
  - Реалізовано метод `find`, який знаходить запис за ім'ям.
  - Реалізовано метод `delete`, який видаляє запис за ім'ям.
- **Record**:
  - Реалізовано зберігання об'єкта `Name` в окремому атрибуті.
  - Реалізовано зберігання списку об'єктів `Phone` в окремому атрибуті.
  - Реалізовано методи для додавання (`add_phone`), видалення (`remove_phone`), редагування (`edit_phone`), пошуку об'єктів `Phone` (`find_phone`).
- **Phone**:
  - Реалізовано валідацію номера телефону (перевірка на 10 цифр).

