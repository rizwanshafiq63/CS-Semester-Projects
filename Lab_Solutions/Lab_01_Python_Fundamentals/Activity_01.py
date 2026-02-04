# Let us take an integer from user as input and check whether the given value is even or not.
# If the given value is not even then it means that it will be odd. 
# So here we need to use if-else statement an demonstrated below.

n = input("Enter a number: ")
if int (n) % 2 == 0:
    print(n,"is an even number.")
else:
    print(n,"is an odd number.")
