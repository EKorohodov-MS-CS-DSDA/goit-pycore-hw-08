from field import Name, Phone, Birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        """
        Adds a phone number to the record.
        Parameters:
            phone (str): The phone number to add.
        """
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Edits a phone number in the record.
        Parameters:
            old_phone (str): The old phone number to edit.
            new_phone (str): The new phone number.
        """
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone: str):
        """
        Finds a phone number in the record.
        Parameters:
            phone (str): The phone number to find.
        Returns:
            str: The phone number if found, None otherwise.
        """
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def remove_phone(self, phone: str):
        """
        Removes a phone number from the record.
        Parameters:
            phone (str): The phone number to remove.
        Raises:
            ValueError: If the phone number is not found in the record.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found in record.")

    def add_birthday(self, birthday: str):
        """
        Adds a birthday to the record.
        Parameters:
            birthday (str): The birthday to add.
        """
        self.birthday = Birthday(birthday)
