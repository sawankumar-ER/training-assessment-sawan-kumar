while True:
    try:
        n = int(input("Enter n: "))
        if n >= 5 and n % 2 == 1:
            break
        print("n must be an odd integer >= 5.")
    except ValueError:
        print("Please enter a valid integer.")

mid = n // 2

for i in range(n):
    k = mid - abs(i - mid) + 1                # right-side stars: 1, 2, ..., mid+1, ..., 2, 1
    gap = "*" * n if i == mid else " " * n    # middle row fills the gap
    print(f" *{gap}{'*' * k}")