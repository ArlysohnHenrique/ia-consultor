from interpretador import obter_cliente


def main() -> None:
    for modelo in obter_cliente().models.list():
        print(modelo.name)


if __name__ == "__main__":
    main()
