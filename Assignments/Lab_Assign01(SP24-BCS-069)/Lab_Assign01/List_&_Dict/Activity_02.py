# A palindrome is a string which is same read forward or backwards.
# For example: "dad" is the same in forward or reverse direction. 
# Another example is "aibohphobia" which literally means, an irritable fear of palindromes.
# Write a function in python that receives a string and returns True if that string is a palindrome and False otherwise.
# Remember that difference between upper and lower case characters are ignored during this determination.

def isPalindrome(word):
    temp = word[::-1]
    if temp.capitalize() == word.capitalize():
        return True
    else:
        return False
    
word = input("Enter a word: ")
print("The word is Palindrome: ", isPalindrome(word))
