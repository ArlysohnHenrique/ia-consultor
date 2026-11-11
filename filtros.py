from collections.abc import Iterable
from typing import Any

from dados import cardapio as CARDAPIO_PADRAO

Prato = dict[str, Any]


def buscar_pratos(
    preco_maximo: float | None = None,
    apenas_vegetarianos: bool = False,
    ingrediente_excluido: str = "",
    cardapio: Iterable[Prato] = CARDAPIO_PADRAO,
) -> list[Prato]:
    """Filtra o cardápio. Sem `preco_maximo`, não há limite de preço."""
    ingrediente_excluido = ingrediente_excluido.strip().casefold()

    return [
        prato
        for prato in cardapio
        if _dentro_do_orcamento(prato, preco_maximo)
        and _atende_preferencia(prato, apenas_vegetarianos)
        and not _contem_ingrediente(prato, ingrediente_excluido)
    ]


def _dentro_do_orcamento(prato: Prato, preco_maximo: float | None) -> bool:
    return preco_maximo is None or prato["preco"] <= preco_maximo


def _atende_preferencia(prato: Prato, apenas_vegetarianos: bool) -> bool:
    return not apenas_vegetarianos or prato["vegetariano"]


def _contem_ingrediente(prato: Prato, ingrediente: str) -> bool:
    return bool(ingrediente) and any(
        ingrediente in item.casefold() for item in prato["ingredientes"]
    )
