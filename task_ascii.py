def ascii_sum(name: str) -> int:
    total = 0
    for ch in name.upper():
        if ch.isalpha():  
            value = ord(ch)
            print(f"{ch} -> {value}")
            total += value
    return total


def digit_sum(n: int) -> int:
    if n < 10:
        return n
    s = sum(int(d) for d in str(n))
    print(f"Digit sum: {' + '.join(str(n))} = {s}")
    return digit_sum(s)


def main():
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    total = ascii_sum(name)
    print(f"Sum = {total}")

    result = digit_sum(total)
    parity = "EVEN" if result % 2 == 0 else "ODD"
    print(f"\nFinal single digit for '{name}': {result} ({parity})")


if __name__ == "__main__":
    main()