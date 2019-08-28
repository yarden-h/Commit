from enum import Enum

# Enums for our request method
class Enum_op(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

# All of my app's custom errors.
class My_Errors(Enum):

	QuoteExists = {"errorCode": 1,"description": "Quote already exist", "level": "Error",}
	QuoteNameInvalid = {"errorCode": 2,"description": "Name is not valid!", "level": "Error",}
	QuotePriceBelowZero = {"errorCode": 3, "description": "Price should not be below 0", "level": "Error",}
	
	UnsupportedMethod = {"errorCode": 10,"description": "Unsupported Method", "level": "Error",}