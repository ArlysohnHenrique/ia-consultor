import unittest

from filtros import buscar_pratos


class TestBuscarPratos(unittest.TestCase):
    def test_filtra_por_preco(self):
        pratos = buscar_pratos(preco_maximo=30)

        ids = {prato["id"] for prato in pratos}

        self.assertEqual(ids, {1, 4, 5})

    def test_filtra_apenas_vegetarianos(self):
        pratos = buscar_pratos(
            preco_maximo=50,
            apenas_vegetarianos=True,
        )

        ids = {prato["id"] for prato in pratos}

        self.assertEqual(ids, {1, 3})

    def test_exclui_ingrediente_sem_diferenciar_maiusculas(self):
        pratos = buscar_pratos(
            preco_maximo=35,
            ingrediente_excluido="  FRANGO  ",
        )

        ids = {prato["id"] for prato in pratos}

        self.assertEqual(ids, {1, 2, 5})

    def test_retorna_lista_vazia_quando_nada_atende(self):
        pratos = buscar_pratos(preco_maximo=10)

        self.assertEqual(pratos, [])

    def test_sem_preco_maximo_nao_limita_preco(self):
        pratos = buscar_pratos()

        ids = {prato["id"] for prato in pratos}

        self.assertEqual(ids, {1, 2, 3, 4, 5})

    def test_aceita_cardapio_customizado(self):
        cardapio = [
            {"id": 99, "preco": 5, "vegetariano": True, "ingredientes": ["pão"]},
        ]

        pratos = buscar_pratos(preco_maximo=10, cardapio=cardapio)

        self.assertEqual([prato["id"] for prato in pratos], [99])


if __name__ == "__main__":
    unittest.main()