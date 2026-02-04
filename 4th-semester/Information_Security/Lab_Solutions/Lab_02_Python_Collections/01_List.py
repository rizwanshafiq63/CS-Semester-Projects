# Python program to demonstrate
# Creation of List

# Creating a List
List = [] 
print("Blank List: ") 
print(List)
# Creating a List of numbers 
List = [10, 20, 14]
print("\nList of numbers: ")
print(List)
# Creating a List of strings and accessing using index
List = ["Geeks", "For", "Geeks"] 
print("\nList Items: ") 
print(List[0])
print(List[2])

# Creating a Multi-Dimensional List 
# (By Nesting a list inside a List) 
List = [['Geeks', 'For'], ['Geeks']] 
print("\nMulti-Dimensional List: ") 
print(List)

# Creating a List with the use of Numbers
# (Having duplicate values) 
List = [1, 2, 4, 4, 3, 3, 3, 6, 5]
print("\nList with the use of Numbers: ") 
print(List)
# Creating a List with mixed type of values
# (Having numbers and strings)
List = [1, 2, 'Geeks', 4, 'For', 6, 'Geeks']
print("\nList with the use of Mixed Values: ") 
print(List)

# Knowing the size of the list
print("\nSize of above list: ")
print(len(List))

# Addition of elements in a List
print("\n--- Addition of elements in a List ---")
# Creating a List 
List = []
print("\nInitial blank List: ")
print(List)
# Addition of Elements in the List 
List.append(1) 
List.append(2) 
List.append(4)
print("\nList after Addition of Three elements: ")
print(List)
# Adding elements to the List # using Iterator
for i in range(1, 4): 
    List.append(i)
print("\nList after Addition of elements from 1-3: ") 
print(List)
# Adding Tuples to the List 
List.append((5, 6))
print("\nList after Addition of a Tuple: ")
print(List)
# Addition of List to a List 
List2 = ['For', 'Geeks'] 
List.append(List2)
print("\nList after Addition of a List: ") 
print(List)

print("\n--- Using the insert() method ---")
# insert() method requires two arguments(position, value).
# Creating a List 
List = [1,2,3,4]
print("Initial List: ")
print(List)
# Addition of Element at specific Position
# (using Insert Method) 
List.insert(3, 12) 
List.insert(0, 'Geeks')
print("\nList after performing Insert Operation: ")
print(List)

print("\n--- Using extend() method ---")
# add multiple elements at the same time at the end of the list.
List = [1, 2, 3, 4]
print("Initial List: ")
print(List)
# Addition of multiple elements to the List at the end
# (using Extend Method) 
List.extend([8, 'Geeks', 'Always'])
print("\nList after performing Extend Operation: ") 
print(List)

# Accessing elements from the List
List = [1, 2, 'Geeks', 4, 'For', 6, 'Geeks']
# accessing an element using negative indexing
print("Accessing element using negative indexing")
# print the last element of list 
print(List[-1])
# print the third
print(List[-3])

print("\n--- Removing elements from list ---")
List = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print("Initial List: ") 
print(List)
# Removing elements from List using Remove() method 
List.remove(5)
List.remove(6)
print("\nList after Removal of two elements: ") 
print(List)
# Removing elements from List using iterator method
for i in range(1, 5): 
    List.remove(i)
print("\nList after Removing a range of elements: ") 
print(List)

print("\n--- Using pop() method ---")
List = [1,2,3,4,5]
# Set using the pop() method
List.pop()
print("\nList after popping an element: ") 
print(List)
# Removing element at a specific location from the Set using the pop() method 
List.pop(2)
print("\nList after popping a specific element: ") 
print(List)

print("\n--- Slicing of List ---")
List = ['G', 'E', 'E', 'K', 'S', 'F', 'O', 'R', 'G', 'E', 'E', 'K', 'S']
print("Initial List: ")
print(List)
# Print elements of a range using Slice operation 
Sliced_List = List[3:8]
print("\nSlicing elements in a range 3-8: ")
print(Sliced_List)
# Print elements from a pre-defined point to end 
Sliced_List = List[5:] 
print("\nElements sliced from 5th element till the end: ") 
print(Sliced_List)
# Printing elements from beginning till end 
Sliced_List = List[:]
print("\nPrinting all elements using slice operation: ") 
print(Sliced_List)

print("\n--- Negative Index List Slicing ---")
List = ['G', 'E', 'E', 'K', 'S', 'F', 'O', 'R', 'G', 'E', 'E', 'K', 'S']
print("Initial List: ")
print(List)
Sliced_List = List[:-6]
print("\nElements sliced till 6th element from last: ") 
print(Sliced_List)
# Print elements of a range using negative index List slicing 
Sliced_List = List[-6:-1]
print("\nElements sliced from index -6 to -1") 
print(Sliced_List)
# Printing elements in reverse using Slice operation 
Sliced_List = List[::-1]
print("\nPrinting List in reverse: ") 
print(Sliced_List)

print("\n--- List Comprehension ---")
print("\nSYNTAX: newList = [ expression(element) for element in oldList if condition ]")
# below list contains square of all odd numbers from range 1 to 10
odd_square = [x ** 2 for x in range(1, 11) if x % 2 == 1]
print(odd_square)
