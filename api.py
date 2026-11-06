from fastapi import FastAPI, HTTPException, Query
from google.genai import errors
from pydantic import BaseModel, Field, ValidationError

from dados import cardapio
from filtros import buscar_pratos
from interpretador import interpretar_pergunta

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

class ConsultaIA(BaseModel):
    pergunta: str = Field(min_length=1, max_length=500)


@app.post("/consultar")
def consultar_com_ia(consulta: ConsultaIA):
    pergunta = consulta.pergunta.strip()

    if not pergunta:
        raise HTTPException(
            status_code=422,
            detail="Informe uma pergunta.",
        )

    try:
        filtros = interpretar_pergunta(pergunta)
    except errors.APIError as erro:
        status = 503 if erro.code in (429, 503) else 502

        raise HTTPException(
            status_code=status,
            detail="O serviço de IA não conseguiu responder. Tente novamente mais tarde.",
        ) from erro
    except ValidationError as erro:
        raise HTTPException(
            status_code=502,
            detail="A IA retornou filtros inválidos.",
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível concluir a interpretação da pergunta.",
        ) from erro

    preco_maximo = filtros.preco_maximo

    if preco_maximo is None:
        preco_maximo = max(
            (prato["preco"] for prato in cardapio),
            default=0,
        )

    pratos = buscar_pratos(
        preco_maximo=preco_maximo,
        apenas_vegetarianos=filtros.apenas_vegetarianos,
        ingrediente_excluido=filtros.ingrediente_excluido,
    )

    return {
        "filtros": filtros.model_dump(),
        "quantidade": len(pratos),
        "pratos": pratos,
    }