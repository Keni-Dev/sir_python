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