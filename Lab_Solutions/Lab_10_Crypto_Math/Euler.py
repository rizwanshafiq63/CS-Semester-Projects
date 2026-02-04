import math

def phi(n): 
    count = 0         
    for k in range(1, n + 1): 
        if math.gcd(n, k) == 1: 
            count += 1 
    return count 

for n in range(1,20) : 
    print("Φ(",n,") = ",phi(n)) 