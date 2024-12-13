# Problem No. 1: Triangular Character Display
char = input("Enter a character: ")
num = int(input("Enter a number: "))

# Upper part
for i in range(1, num + 1):
    print(char * i)
# Lower part
for i in range(num - 1, 0, -1):
    print(char * i)

print()  # Add a blank line for separation

# Problem No. 2: Sum of Cubes
while 1:
    try:
        num = int(input("Enter a number: "))
        result=0
        for i in range(1,num):
            result += i**3
        print(f"The sum of all cubes is {result}.")
        break
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        continue

print()  # Add a blank line for separation

# Problem No. 3: Continuous Number Triangle
while 1:
    try:
        max_num = int(input("Enter a number: "))
        current = 1

        for i in range(1, max_num + 1):
            for j in range(i):
                if current > max_num:
                    break
                print(current, end="")
                current += 1
            if current <= max_num or j == i - 1:  # Only print a new line if numbers were printed
                print()
        break
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        continue

print()  # Add a blank line for separation

# Problem No. 4: Sum, Average, and Square Root of Odd Numbers
sum_odd = 0
count_odd = 0

while 1:
    try:
        num = int(input("Enter a number. 0 to exit: "))
        if num == 0:
            if count_odd == 0:
                print("Exception has occured: ZeroDivisionError")
                break
            avg = sum_odd / count_odd
            sqrt = sum_odd ** 0.5
            print(f"The sum of all odd numbers is {sum_odd}.")
            print(f"The average of all odd numbers is {avg:.2f}.")
            print(f"The square root of the sum of all odd numbers is {sqrt:.2f}.")
            break
        elif num % 2 != 0:
            sum_odd += num
            count_odd += 1
    except ValueError:
        print("Invalid input! Please enter a valid number.")

print()  # Add a blank line for separation

# Problem No. 5: Pyramid Height
try:
    blocks = int(input("Enter the number of blocks: "))
    height = 0
    layer = 1

    while blocks >= layer:
        blocks -= layer
        height += 1
        layer += 1

    print(f"The height of the pyramid is {height}.")
except ValueError:
    print("Invalid input! Please enter a valid number.")