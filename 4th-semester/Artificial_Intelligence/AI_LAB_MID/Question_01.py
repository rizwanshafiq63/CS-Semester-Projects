
# PART A ANSWER
data = [1,2,3,4,5,6,7,8,9,10,11,12]
data1 = []
data2 = []

eightyPercent = round(80 / 100 * len(data))

print(eightyPercent)
count = 0
while(count < len(data)):
    if count < eightyPercent:
        data1.append(data[count])
    else:
        data2.append(data[count])
    count += 1

print("data1 = ", data1)
print("data2 = ", data2)

# PART B ANSWER
n = int(input("Enter the no of terms: "))

pi = 0
sign = 1

for i in range(n):
    pi += sign * (1 / (2*i+1))
    sign *= -1
    
    
pi *= 4

print("Value of pi = ", pi)
