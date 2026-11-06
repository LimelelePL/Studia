from app.decorators import log_test, require


def main() -> None:
    # log_test_class()
    log_test()

    @require
    def funckja(arg):
        print("elo")

    funckja(None)


if __name__ == "__main__":
    main()
