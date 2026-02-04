# Accept two lists from user and display their join.

myList1 = []
print("Enter objects of first list...")
for i in range(5):
    val = input("Enter a value; ")
    n = int(val)
    myList1.append(n)
    
myList2 = []
print("Enter objects of second list...")
for i in range(5):
    val = input("Enter a value; ")
    n = int(val)
    myList2.append(n)
    
list3 = myList1 + myList2
print(list3)
