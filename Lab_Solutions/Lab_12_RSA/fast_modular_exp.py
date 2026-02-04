def fast_mod_exp(base, exponent, modulus): 
    """ 
    Compute (base^exponent) mod modulus efficiently 
    Time Complexity: O(log exponent) 
    """ 
    result = 1 
    base = base % modulus 

    while exponent > 0: 
        # If exponent is odd, multiply base with result 
        if exponent % 2 == 1: 
            result = (result * base) % modulus 

        # Square the base 
        base = (base * base) % modulus 

        # Divide exponent by 2 
        exponent = exponent // 2 

    return result 

# Example: Compute 123^17 mod 3233 
result = fast_mod_exp(123, 17, 3233) 
print(f"123^17 mod 3233 = {result}")  # Output: 855