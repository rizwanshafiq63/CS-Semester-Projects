# Create a Python program that contains a dictionary of names and phone numbers. 
# Use a tuple of separate first and last name values for the key field. 
# Initialize the dictionary with at least three names and numbers.
# Ask the user to search for a phone number by entering a first and last name. 
# Display the matching number if found, or a message if not found.

sample = {("sohaib","ali"):"03001234567", 
          ("saim","hassan"):"03001234568",
          ("taha","shahbaz"):"03001234569", }

firstName = input("Enter first name: ")
lastName = input("Enter last name: ")

searchTuple = (firstName, lastName)
if searchTuple in sample:
    print("Phone#",sample[searchTuple])
else:
    print("Name NOT found")
