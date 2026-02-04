# Create two lists based on the user values.
# Merge both the lists and display in sorted order.

# Taking input from user
list1 = list(map(int, input("Enter numbers for first list (separated by spaces): ").split()))
list2 = list(map(int, input("Enter numbers for second list (separated by spaces): ").split()))

# Merging lists
merged_list = list1 + list2

# Sorting the merged list
merged_list.sort()

# # Bubble sort
# n = len(merged_list)
# for i in range(n):
#     for j in range(0, n-i-1):
#         if merged_list[j] > merged_list[j+1]:
#             merged_list[j], merged_list[j+1] = merged_list[j+1], merged_list[j]

print("Merged and Sorted List:", merged_list)
