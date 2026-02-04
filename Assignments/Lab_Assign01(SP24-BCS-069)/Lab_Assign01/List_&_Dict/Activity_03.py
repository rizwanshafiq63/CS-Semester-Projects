# Imagine two matrices given in the form of 2D lists as under; 
a = [[1, 0, 0],
     [0, 1, 0], 
     [0, 0, 1] ]
b = [[1, 2, 3],
     [4, 5, 6], 
     [7, 8, 9] ]
# Write a python code that finds another matrix/2D list that is a product of a and b, i.e., C=a*b
c = []

c = []

for indrow in range(3):                 # loop over rows of A
     c.append([])                        # add a new row in result C
     for indcol in range(3):             # loop over columns of B
          c[indrow].append(0)             # start with 0 in C[indrow][indcol]
          for indaux in range(3):         # loop for dot product
               c[indrow][indcol] += a[indrow][indaux] * b[indaux][indcol]

print(c)
