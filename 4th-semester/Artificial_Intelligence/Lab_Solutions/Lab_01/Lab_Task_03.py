# Fibonacci series is that when you add the previous two numbers the next number is formed.
# You have to start from 0 and 1. E.g. 0+1=1 → 1+1=2 → 1+2=3 → 2+3=5 → 3+5=8 → 5+8=13
# So the series becomes 0 1 1 2 3 5 8 13 21 34 55 ……………………………………
# Steps: You have to take an input number that shows how many terms to be displayed. 
# Then use loops for displaying the Fibonacci series up to that term.
# E.g. input no is 6 the output should be 0 1 1 2 3 5

terms = int(input("Enter number of Fibonacci terms you want: "))

a, b = 0, 1
print("Fibonacci Series:")

for i in range(terms):
    print(a, end = " ")
    temp = a + b   
    a = b          
    b = temp       
