from fastapi import FastAPI, Query

from filtros import buscar_pratos

app = FastAPI(
    title="Assistente de Cardápio",
    description="API para consultar um cardápio fictício.",
    version="0.1.0",
)


@app.get("/pratos")
def listar_pratos(
    preco_maximo: float = Query(default=100, ge=0),
    apenas_vegetarianos: bool = False,
    ingrediente_excluido: str = "",
):
    pratos = buscar_pratos(
        preco_maximo=preco_maximo,
        apenas_vegetarianos=apenas_vegetarianos,
        ingrediente_excluido=ingrediente_excluido,
    )

    return {
        "quantidade": len(pratos),
        "pratos": pratos,
    }