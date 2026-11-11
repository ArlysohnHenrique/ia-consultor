from filtros import buscar_pratos
from interpretador import interpretar_pergunta


def main() -> None:
    pergunta = input("O que você gostaria de comer? ")
    filtros = interpretar_pergunta(pergunta)

    pratos = buscar_pratos(
        preco_maximo=filtros.preco_maximo,
        apenas_vegetarianos=filtros.apenas_vegetarianos,
        ingrediente_excluido=filtros.ingrediente_excluido,
    )

    print("\nFiltros interpretados:")
    print(filtros.model_dump_json(indent=2))

    print("\nPratos encontrados:")

    if not pratos:
        print("Nenhum prato atende aos filtros informados.")
        return

    for prato in pratos:
        print(f'{prato["nome"]} — R$ {prato["preco"]:.2f}')


if __name__ == "__main__":
    main()
