# Problem No. 1
try: n1, n2 = map(int, input("Enter two numbers: ").split()); print(str(n1) * n2)
except ValueError: print("Invalid input. Please enter integers.")

#2 lines
#n1, n2 = map(int, input("Enter two numbers: ").split())
#print(str(n1) * n2)

print()  # Add a blank line for separation

# Problem No. 2
try:
    h = int(input("Enter height: "))
    if h < 2: raise ValueError
    print("+{}+".format("=" * 10)); [print("+          +") for _ in range(h - 2)]; print("+{}+".format("=" * 10))
except ValueError: print("Invalid height. Enter an integer >= 2.")
# added error handling to continue program if the input is error
#4 lines without error handling
#h = int(input("Enter height: "))
#print("+{}+".format("=" * 10))
#for _ in range(h - 2): print("+          +")
#print("+{}+".format("=" * 10))

print()  # Add a blank line for separation

# Problem No. 3
try:
    n1, n2 = map(int, input("Enter two numbers: ").split())
    print(f"The sum of all three numbers are {(n1 * n2) + n2 + (n2 * 6)}.")
except ValueError: print("Invalid input. Please enter integers.")

print()  # Add a blank line for separation

# Problem No. 4
while(1):
    try:
        num1 = int(input("Enter an integer: "))
        num2 = float(input("Enter a float: "))
        print("First Number: %.2f, Second Number: %d" % (num1, num2))
        print(f'First Number: {num1:.2f}, Second Number: {int(num2)}')
        break
    except ValueError: 
        print("Invalid input. Ensure the first is an integer and the second is a float.")
        continue

print()  # Add a blank line for separation

# Problem No. 5
sep = input("Enter separator character/s: ")
end = input("Enter ending character/s: ")
print("I", "love", "Python", sep=sep*2, end=end)