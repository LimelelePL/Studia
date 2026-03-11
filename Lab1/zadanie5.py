import pyfiglet

if __name__ == "__main__":
    user_string = input("Podaj napis do sformatowania: ")
    print(pyfiglet.figlet_format(user_string))
