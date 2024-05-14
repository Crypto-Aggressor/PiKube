from mpmath import mp
from colorama import Fore, Style

"""
This script prints the number pi to a specified precision with certain digits colored to 
create a visual representation of the pi symbol and a cube. It uses the mpmath library 
to calculate pi and colorama to add color to the terminal output.

"""

# Set the frame
y = 25

# Line breaker
x = 111

# Set the desired precision (number of decimal places)
precision = y * x

# Set the value of PI with the desired precision
mp.dps = precision
pi_value = str(mp.pi)

# Print the PI number with 'x * y' decimals
# Highlighting decimals to draw PI in red
for i, char in enumerate(pi_value):
    if (x * 0 + 0 <= i < x * 0 + 4) \
    or (x * 2 + 11 <= i < x * 2 + 56) \
    or (x * 3 + 8 <= i < x * 3 + 56) \
    or (x * 4 + 6 <= i < x * 4 + 56) \
    or (x * 5 + 4 <= i < x * 5 + 56) \
    or (x * 6 + 3 <= i < x * 6 + 7) or (x * 6 + 16 <= i < x * 6 + 22) or (x * 6 + 37 <= i < x * 6 + 43) \
    or (x * 7 + 2 <= i < x * 7 + 5) or (x * 7 + 16 <= i < x * 7 + 22) or (x * 7 + 37 <= i < x * 7 + 43) \
    or (x * 8 + 2 <= i < x * 8 + 4) or (x * 8 + 15 <= i < x * 8 + 21) or (x * 8 + 36 <= i < x * 8 + 42) \
    or (x * 9 + 2 <= i < x * 9 + 3) or (x * 9 + 14 <= i < x * 9 + 20) or (x * 9 + 35 <= i < x * 9 + 41) \
    or (x * 10 + 14 <= i < x * 10 + 20) or (x * 10 + 35 <= i < x * 10 + 41) \
    or (x * 11 + 14 <= i < x * 11 + 20) or (x * 11 + 35 <= i < x * 11 + 41) \
    or (x * 12 + 14 <= i < x * 12 + 20) or (x * 12 + 35 <= i < x * 12 + 41) \
    or (x * 13 + 13 <= i < x * 13 + 19) or (x * 13 + 35 <= i < x * 13 + 41) \
    or (x * 14 + 13 <= i < x * 14 + 19) or (x * 14 + 35 <= i < x * 14 + 41) \
    or (x * 15 + 13 <= i < x * 15 + 19) or (x * 15 + 35 <= i < x * 15 + 41) \
    or (x * 16 + 12 <= i < x * 16 + 19) or (x * 16 + 35 <= i < x * 16 + 41) \
    or (x * 17 + 11 <= i < x * 17 + 18) or (x * 17 + 35 <= i < x * 17 + 41) or (x * 17 + 53 <= i < x * 17 + 54) \
    or (x * 18 + 10 <= i < x * 18 + 18) or (x * 18 + 35 <= i < x * 18 + 42) or (x * 18 + 52 <= i < x * 18 + 54) \
    or (x * 19 + 8 <= i < x * 19 + 17) or (x * 19 + 35 <= i < x * 19 + 43) or (x * 19 + 50 <= i < x * 19 + 54) \
    or (x * 20 + 6 <= i < x * 20 + 17) or (x * 20 + 35 <= i < x * 20 + 53) \
    or (x * 21 + 6 <= i < x * 21 + 16) or (x * 21 + 36 <= i < x * 21 + 52) \
    or (x * 22 + 6 <= i < x * 22 + 15) or (x * 22 + 38 <= i < x * 22 + 50) \
    or (x * 23 + 8 <= i < x * 23 + 13) or (x * 23 + 41 <= i < x * 23 + 48):
        print(f"{Fore.RED}{char}{Style.RESET_ALL}", end="")
        
    # Highlighting decimals to draw THON in blue
    elif (x * 2 + 58 <= i < x * 2 + 66) \
    or (x * 3 + 61 <= i < x * 3 + 63) \
    or (x * 4 + 61 <= i < x * 4 + 63) \
    or (x * 5 + 61 <= i < x * 5 + 63) \
    or (x * 7 + 58 <= i < x * 7 + 60) or (x * 7 + 64 <= i < x * 7 + 66) \
    or (x * 8 + 58 <= i < x * 8 + 60) or (x * 8 + 64 <= i < x * 8 + 66) \
    or (x * 9 + 58 <= i < x * 9 + 66) \
    or (x * 10 + 58 <= i < x * 10 + 60) or (x * 10 + 64 <= i < x * 10 + 66) \
    or (x * 11 + 58 <= i < x * 11 + 60) or (x * 11 + 64 <= i < x * 11 + 66) \
    or (x * 13 + 60 <= i < x * 13 + 64) \
    or (x * 14 + 58 <= i < x * 14 + 60) or (x * 14 + 64 <= i < x * 14 + 66) \
    or (x * 15 + 58 <= i < x * 15 + 60) or (x * 15 + 64 <= i < x * 15 + 66) \
    or (x * 16 + 58 <= i < x * 16 + 60) or (x * 16 + 64 <= i < x * 16 + 66) \
    or (x * 17 + 60 <= i < x * 17 + 64) \
    or (x * 19 + 58 <= i < x * 19 + 61) or (x * 19 + 64 <= i < x * 19 + 66) \
    or (x * 20 + 58 <= i < x * 20 + 60) or (x * 20 + 61 <= i < x * 20 + 62) or (x * 20 + 64 <= i < x * 20 + 66) \
    or (x * 21 + 58 <= i < x * 21 + 60) or (x * 21 + 62 <= i < x * 21 + 63) or (x * 21 + 64 <= i < x * 21 + 66) \
    or (x * 22 + 58 <= i < x * 22 + 60) or (x * 22 + 63 <= i < x * 22 + 64) or (x * 22 + 64 <= i < x * 22 + 66):
        print(f"{Fore.BLUE}{char}{Style.RESET_ALL}", end="")
    
    # Highlighting decimals to create the front face of a cube in green
    elif (x * 2 + 73 <= i < x * 2 + 109) \
    or (x * 3 + 72 <= i < x * 3 + 73) or (x * 3 + 106 <= i < x * 2 + 107) or (x * 3 + 108 <= i < x * 3 + 109) \
    or (x * 4 + 71 <= i < x * 4 + 72) or (x * 4 + 105 <= i < x * 4 + 106) or (x * 4 + 108 <= i < x * 4 + 109) \
    or (x * 5 + 70 <= i < x * 5 + 71) or (x * 5 + 104 <= i < x * 5 + 105) or (x * 5 + 108 <= i < x * 5 + 109) \
    or (x * 6 + 69 <= i < x * 6 + 70) or (x * 6 + 103 <= i < x * 6 + 104) or (x * 6 + 108 <= i < x * 6 + 109) \
    or (x * 7 + 68 <= i < x * 7 + 103) or (x * 7 + 108 <= i < x * 7 + 109) \
    or (x * 8 + 68 <= i < x * 8 + 70) or (x * 8 + 101 <= i < x * 8 + 103) or (x * 8 + 108 <= i < x * 8 + 109) \
    or (x * 9 + 68 <= i < x * 9 + 70) or (x * 9 + 101 <= i < x * 9 + 103) or (x * 9 + 108 <= i < x * 9 + 109) \
    or (x * 10 + 68 <= i < x * 10 + 70) or (x * 10 + 101 <= i < x * 10 + 103) or (x * 10 + 108 <= i < x * 10 + 109) \
    or (x * 11 + 68 <= i < x * 11 + 70) or (x * 11 + 101 <= i < x * 11 + 103) or (x * 11 + 108 <= i < x * 11 + 109) \
    or (x * 12 + 68 <= i < x * 12 + 70) or (x * 12 + 101 <= i < x * 12 + 103) or (x * 12 + 108 <= i < x * 12 + 109) \
    or (x * 13 + 68 <= i < x * 13 + 70) or (x * 13 + 101 <= i < x * 13 + 103) or (x * 13 + 108 <= i < x * 13 + 109) \
    or (x * 14 + 68 <= i < x * 14 + 70) or (x * 14 + 101 <= i < x * 14 + 103) or (x * 14 + 108 <= i < x * 14 + 109) \
    or (x * 15 + 68 <= i < x * 15 + 70) or (x * 15 + 101 <= i < x * 15 + 103) or (x * 15 + 108 <= i < x * 15 + 109) \
    or (x * 16 + 68 <= i < x * 16 + 70) or (x * 16 + 101 <= i < x * 16 + 103) or (x * 16 + 108 <= i < x * 16 + 109) \
    or (x * 17 + 68 <= i < x * 17 + 70) or (x * 17 + 101 <= i < x * 17 + 109) \
    or (x * 18 + 68 <= i < x * 18 + 70) or (x * 18 + 101 <= i < x * 18 + 103) or (x * 18 + 107 <= i < x * 18 + 108) \
    or (x * 19 + 68 <= i < x * 19 + 70) or (x * 19 + 101 <= i < x * 19 + 103) or (x * 19 + 106 <= i < x * 19 + 107) \
    or (x * 20 + 68 <= i < x * 20 + 70) or (x * 20 + 101 <= i < x * 20 + 103) or (x * 20 + 105 <= i < x * 20 + 106) \
    or (x * 21 + 68 <= i < x * 21 + 70) or (x * 21 + 101 <= i < x * 21 + 103) or (x * 21 + 104 <= i < x * 21 + 105) \
    or (x * 22 + 68 <= i < x * 22 + 104):
        print(f"{Fore.BLUE}{char}{Style.RESET_ALL}", end="")
        
        # Highlighting decimals to create the back face of a cube in cyan
    elif (x * 3 + 73 <= i < x * 3 + 74) \
    or (x * 4 + 73 <= i < x * 4 + 74) \
    or (x * 5 + 73 <= i < x * 5 + 74) \
    or (x * 6 + 73 <= i < x * 6 + 74)  \
    or (x * 7 + 73 <= i < x * 7 + 74)  \
    or (x * 8 + 73 <= i < x * 8 + 74)  \
    or (x * 9 + 73 <= i < x * 9 + 74)  \
    or (x * 10 + 73 <= i < x * 10 + 74) \
    or (x * 11 + 73 <= i < x * 11 + 74) \
    or (x * 12 + 73 <= i < x * 12 + 74) \
    or (x * 13 + 73 <= i < x * 13 + 74) \
    or (x * 14 + 73 <= i < x * 14 + 74) \
    or (x * 15 + 73 <= i < x * 15 + 74) \
    or (x * 16 + 73 <= i < x * 16 + 74) \
    or (x * 17 + 73 <= i < x * 17 + 109) \
    or (x * 18 + 72 <= i < x * 18 + 73) \
    or (x * 19 + 71 <= i < x * 19 + 72) \
    or (x * 20 + 70 <= i < x * 20 + 71) \
    or (x * 21 + 69 <= i < x * 21 + 70):
        print(f"{Fore.CYAN}{char}{Style.RESET_ALL}", end="")
        
    else:
        print(char, end="")
    
    if (i + 1) % x  == 0:
        print(' ')