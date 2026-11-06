from dados import cardapio

def buscar_pratos(
    preco_maximo,
    apenas_vegetarianos=False,
    ingrediente_excluido="",
):
    resultados = []
    ingrediente_excluido = ingrediente_excluido.strip().casefold()

    for prato in cardapio:
        dentro_do_orcamento = prato["preco"] <= preco_maximo

        atende_preferencia = (
            not apenas_vegetarianos or prato["vegetariano"]
        )

        contem_ingrediente = (
            bool(ingrediente_excluido)
            and any(
                ingrediente_excluido in ingrediente.casefold()
                for ingrediente in prato["ingredientes"]
            )
        )

        if dentro_do_orcamento and atende_preferencia and not contem_ingrediente:
            resultados.append(prato)

    return resultados