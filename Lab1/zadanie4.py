import pyfiglet


def get_user_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Podano niepoprawną wartość. Podaj liczbę całkowitą")


def calculate_triangle_area(base: int, height: int) -> float:
    if base <= 0:
        raise ValueError(f"Podstawa musi być liczbą dodatnią, podano {base}")
    if height <= 0:
        raise ValueError(f"Wysokośc musi być liczbą dodatnią, podano {height}")
    return (base * height) / 2


if __name__ == "__main__":
    print(pyfiglet.figlet_format("Program do liczenia pola trójkąta"))
    height = get_user_int("Podaj wysokość trojkąta: ")
    base = get_user_int("Podaj długośc podstawy trójkąta: ")
    area = calculate_triangle_area(base, height)
    print(f"Pole trójkąta jest równe: {area}")
