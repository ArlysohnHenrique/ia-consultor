from filtros import buscar_pratos

try:
    preco_maximo = float(
        input("Qual o valor máximo que deseja gastar? R$ ").replace(",", ".")
    )

    if preco_maximo < 0:
        print("O valor não pode ser negativo.")
    else:
        resposta = input("Apenas pratos vegetarianos? (s/n): ").strip().lower()

        if resposta not in ("s", "n"):
            print("Resposta inválida. Digite s ou n.")
        else:
            ingrediente_excluido = input("Qual ingrediente deseja evitar? Enter para nenhum: ")

            pratos = buscar_pratos(
            preco_maximo=preco_maximo,
            apenas_vegetarianos=resposta == "s",
            ingrediente_excluido=ingrediente_excluido,
        )

            if not pratos:
                print("Nenhum prato encontrado para os filtros informados.")
            else:
                for prato in pratos:
                    print(f'{prato["nome"]} — R$ {prato["preco"]:.2f}')

except ValueError:
    print("Valor inválido. Digite um número, como 30 ou 28,90.")