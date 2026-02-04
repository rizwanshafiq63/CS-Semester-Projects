# Lab Task 3: For this exercise, you will keep track of when our friend’s birthdays are, and be able to find that information based on their name. 
# Create a dictionary (in your file) of names and birthdays. 
# When you run your program it should ask the user to enter a name, and return the birthday of that person back to them. 
# The interaction should look something like this:
# >>> Welcome to the birthday dictionary. We know the birthdays of: Albert Einstein Benjamin Franklin Ada Lovelace
# >>> Who's birthday do you want to look up? 
# Benjamin Franklin
# >>> Benjamin Franklin's birthday is 01/17/1706.

# Dictionary of names and birthdays
birthdays = {
    "Albert Einstein": "03/14/1879",
    "Benjamin Franklin": "01/17/1706",
    "Ada Lovelace": "12/10/1815"
}

print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in birthdays:
    print(name)

# Asking user for a name
person = input("Who's birthday do you want to look up? ")

# Displaying result
if person in birthdays:
    print(f"{person}'s birthday is {birthdays[person]}.")
else:
    print("Sorry, we don't have that person's birthday in the dictionary.")
