# Imagine two sets A and B containing numbers. 
# Without using built-in set functionalities, write your own function that receives two such sets and returns another set C which is a symmetric difference of the two input sets. 
# (A symmetric difference between A and B will return a set C which contains only those items that appear in one of A or B. 
# Any items that appear in both sets are not included in C). 
# Now compare the output of your function with the following built-in functions/operators.
#  A.symmetric_difference(B)
#  B.symmetric_difference(A)
#  A ^ B
#  B ^ A

def symmDiff(a,b):
    empty_set = set() # empty set
    for i in a: # for loop used to access in a
        if i not in b:
            empty_set.add(i)
    for i in b: # for loop used to access in b
        if i not in a:
            empty_set.add(i)
    return empty_set

set1 = {0,1,2,4,5}
set2 = {4,5,7,8,9}
print(symmDiff(set1, set2))

# verification using inbuilt function
print(set1.symmetric_difference(set2))
print(set2.symmetric_difference(set1))
print(set1^set2)
print(set2^set1)
