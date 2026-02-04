# A closed polygon with N sides can be represented as a list of tuples of N connected coordinates, 
# i.e., [ (x1,y1), (x2,y2), (x3,y3), . . . , (xN,yN) ]. 
# A sample polygon with 6 sides (N=6) is shown below.
# Write a python function that takes a list of N tuples as input 
# and returns the perimeter of the polygon. 
# Remember that your code should work for any value of N.
# Hint: A perimeter is the sum of all sides of a polygon.

def perimeter(listing):
    leng = len(listing)
    perimeter = 0
    for i in range(0, leng - 1):
        dist = (((listing[i][0] - listing[i+1][0]) ** 2) + 
                ((listing[i][1] - listing[i+1][1]) ** 2)) ** 0.5
        perimeter = perimeter + dist
    perimeter = perimeter + (((listing[0][0] - listing[leng-1][0]) ** 2) + 
                ((listing[0][1] - listing[leng-1][1]) ** 2)) ** 0.5
    return perimeter

L = [(1,3), (2,7), (3,9), (-1,8)]
print(perimeter(L))
