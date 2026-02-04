n = int(input("Enter a number: "))

# Count digits
temp = n
digits = 0
while temp > 0:
    digits += 1
    temp //= 10

# Even case: reverse normally
if n % 2 == 0:
    temp = n
    rev = 0
    while temp > 0:
        rev = rev * 10 + temp % 10
        temp //= 10
    print(rev)

# Odd case: reverse but skip middle digit
else:
    temp = n
    rev = 0
    pos = 0
    middle = digits // 2 
    while temp > 0:
        d = temp % 10
        if pos != middle:      
            rev = rev * 10 + d
        pos += 1
        temp //= 10
    print(rev)
