from datetime import datetime

class Field:
    """
    A base entity class that represents a field in the address book.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Represents a name field.
    """
    pass


class Phone(Field):
    """
    Represents a phone field.
    """
    def __init__(self, value):
        self.value = self.validated_phone(value)

    def validated_phone(self, phone: str) -> str:
        """
        Validates the phone number.
        Parameters:
            phone (str): The phone number to validate.
        Returns:
            str: The validated phone number.
        Raises:
            ValueError: If the phone number is not 10 digits long or 
            if it contains non-digit characters.
        """
        if not len(phone) == 10 and phone.isdigit():
            raise ValueError("Invalid phone number: {phone}. Must be 10-digits long.")
        return phone


class Birthday(Field):
    """
    Represents a birthday field.
    """
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
