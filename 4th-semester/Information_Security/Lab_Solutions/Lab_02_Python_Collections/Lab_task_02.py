# Repeat the previous activity to find the smallest and largest element of the list. (Suppose all the elements are integer values)

# Taking input from user
list1 = list(map(int, input("Enter numbers for first list (separated by spaces): ").split()))
list2 = list(map(int, input("Enter numbers for second list (separated by spaces): ").split()))

# Merging lists
merged_list = list1 + list2

# Sorting for display
merged_list.sort()

print("Merged and Sorted List:", merged_list)
print("Smallest Element:", min(merged_list))
print("Largest Element:", max(merged_list))
