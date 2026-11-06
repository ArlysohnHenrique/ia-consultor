import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app
from interpretador import FiltrosBusca


class TestConsultaIA(unittest.TestCase):
    def setUp(self):
        self.cliente = TestClient(app)

    @patch("api.interpretar_pergunta")
    def test_consulta_filtra_pratos(self, interpretar_mock):
        interpretar_mock.return_value = FiltrosBusca(
            preco_maximo=35,
            apenas_vegetarianos=True,
            ingrediente_excluido="queijo",
        )

        resposta = self.cliente.post(
            "/consultar",
            json={
                "pergunta": "Quero algo vegetariano até 35 reais, sem queijo"
            },
        )

        self.assertEqual(resposta.status_code, 200)

        dados = resposta.json()
        ids = {prato["id"] for prato in dados["pratos"]}

        self.assertEqual(ids, {1})
        self.assertEqual(dados["quantidade"], 1)

        interpretar_mock.assert_called_once_with(
            "Quero algo vegetariano até 35 reais, sem queijo"
        )

    @patch("api.interpretar_pergunta")
    def test_rejeita_pergunta_em_branco(self, interpretar_mock):
        resposta = self.cliente.post(
            "/consultar",
            json={"pergunta": "   "},
        )

        self.assertEqual(resposta.status_code, 422)
        interpretar_mock.assert_not_called()

    @patch("api.interpretar_pergunta")
    def test_consulta_sem_limite_de_preco(self, interpretar_mock):
        interpretar_mock.return_value = FiltrosBusca(
            preco_maximo=None,
            apenas_vegetarianos=False,
            ingrediente_excluido="frango",
        )

        resposta = self.cliente.post(
            "/consultar",
            json={"pergunta": "Quero pratos sem frango"},
        )

        self.assertEqual(resposta.status_code, 200)

        ids = {
            prato["id"]
            for prato in resposta.json()["pratos"]
        }

        self.assertEqual(ids, {1, 2, 3, 5})


if __name__ == "__main__":
    unittest.main()