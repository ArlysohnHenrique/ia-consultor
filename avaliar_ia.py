from interpretador import interpretar_pergunta


casos = [
    {
        "pergunta": "Quero algo vegetariano até 35 reais, sem queijo",
        "esperado": {
            "preco_maximo": 35,
            "apenas_vegetarianos": True,
            "ingrediente_excluido": "queijo",
        },
    },
    {
        "pergunta": "Quero gastar no máximo 25 reais",
        "esperado": {
            "preco_maximo": 25,
            "apenas_vegetarianos": False,
            "ingrediente_excluido": "",
        },
    },
    {
        "pergunta": "Quero pratos sem frango",
        "esperado": {
            "preco_maximo": None,
            "apenas_vegetarianos": False,
            "ingrediente_excluido": "frango",
        },
    },
    {
        "pergunta": "Pode ter carne, até 32 reais",
        "esperado": {
            "preco_maximo": 32,
            "apenas_vegetarianos": False,
            "ingrediente_excluido": "",
        },
    },
    {
        "pergunta": "Só pratos vegetarianos, sem limite de preço",
        "esperado": {
            "preco_maximo": None,
            "apenas_vegetarianos": True,
            "ingrediente_excluido": "",
        },
    },
]


def normalizar(filtros):
    return {
        **filtros,
        "ingrediente_excluido": (
            filtros["ingrediente_excluido"].strip().casefold()
        ),
    }


def avaliar():
    acertos = 0
    erros_servico = 0

    for numero, caso in enumerate(casos, start=1):
        print(f'\nCaso {numero}: {caso["pergunta"]}')

        try:
            obtido = interpretar_pergunta(
                caso["pergunta"]
            ).model_dump()
        except Exception as erro:
            erros_servico += 1
            print(f"ERRO DE EXECUÇÃO: {type(erro).__name__}")
            continue

        correto = normalizar(obtido) == normalizar(caso["esperado"])

        if correto:
            acertos += 1
            print("ACERTO")
        else:
            print("DIVERGÊNCIA")
            print("Esperado:", caso["esperado"])
            print("Obtido:  ", obtido)

    print(f"\nAcertos completos: {acertos}/{len(casos)}")
    print(f"Erros de execução: {erros_servico}")


if __name__ == "__main__":
    avaliar()