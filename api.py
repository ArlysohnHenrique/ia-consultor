import logging
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, RedirectResponse
from google.genai import errors
from pydantic import BaseModel, Field, ValidationError

from config import ConfiguracaoAusenteError
from filtros import buscar_pratos
from interpretador import (
    FiltrosBusca,
    RespostaVaziaError,
    interpretar_audio,
    interpretar_pergunta,
)

app = FastAPI(
    title="Assistente de Cardápio",
    description="API para consultar um cardápio fictício.",
    version="0.1.0",
)

logger = logging.getLogger("uvicorn.error")

PAGINA_CHAT = Path(__file__).with_name("static") / "chat.html"

TAMANHO_MAXIMO_AUDIO = 5 * 1024 * 1024  # 5 MB, cerca de 2 min de WAV 16 kHz mono

# Formatos de áudio aceitos pelo Gemini, com os apelidos usados pelos navegadores.
FORMATOS_AUDIO = {
    "audio/wav": "audio/wav",
    "audio/wave": "audio/wav",
    "audio/x-wav": "audio/wav",
    "audio/mp3": "audio/mp3",
    "audio/mpeg": "audio/mp3",
    "audio/aiff": "audio/aiff",
    "audio/aac": "audio/aac",
    "audio/ogg": "audio/ogg",
    "audio/flac": "audio/flac",
}


@app.get("/", include_in_schema=False)
def raiz():
    return RedirectResponse("/chat")


@app.get("/chat", include_in_schema=False)
def chat():
    """Interface de chat para testar as rotas de consulta no navegador."""
    return FileResponse(PAGINA_CHAT, media_type="text/html")


@app.get("/pratos", tags=["Cardápio"], summary="Listar pratos com filtros")
def listar_pratos(
    preco_maximo: float | None = Query(default=None, ge=0),
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


@contextmanager
def erros_da_ia() -> Iterator[None]:
    """Converte falhas da integração com a IA em respostas HTTP."""
    try:
        yield
    except ConfiguracaoAusenteError as erro:
        raise HTTPException(
            status_code=500,
            detail="O serviço de IA não está configurado no servidor.",
        ) from erro
    except errors.APIError as erro:
        logger.warning("Falha na API do Gemini (%s): %s", erro.code, erro.message)
        status = 503 if erro.code in (429, 503) else 502

        raise HTTPException(
            status_code=status,
            detail="O serviço de IA não conseguiu responder. Tente novamente mais tarde.",
        ) from erro
    except RespostaVaziaError as erro:
        raise HTTPException(
            status_code=502,
            detail="A IA não retornou uma resposta.",
        ) from erro
    except ValidationError as erro:
        raise HTTPException(
            status_code=502,
            detail="A IA retornou filtros inválidos.",
        ) from erro


def resultado_da_busca(filtros: FiltrosBusca) -> dict:
    pratos = buscar_pratos(
        preco_maximo=filtros.preco_maximo,
        apenas_vegetarianos=filtros.apenas_vegetarianos,
        ingrediente_excluido=filtros.ingrediente_excluido,
    )

    return {
        "filtros": filtros.model_dump(),
        "quantidade": len(pratos),
        "pratos": pratos,
    }


@app.post("/consultar", tags=["Consulta com IA"], summary="Consultar por texto")
def consultar_com_ia(consulta: ConsultaIA):
    pergunta = consulta.pergunta.strip()

    if not pergunta:
        raise HTTPException(
            status_code=422,
            detail="Informe uma pergunta.",
        )

    with erros_da_ia():
        filtros = interpretar_pergunta(pergunta)

    return resultado_da_busca(filtros)


@app.post(
    "/consultar-audio",
    tags=["Consulta com IA"],
    summary="Consultar por áudio",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                formato: {"schema": {"type": "string", "format": "binary"}}
                for formato in sorted(set(FORMATOS_AUDIO.values()))
            },
        }
    },
)
async def consultar_por_audio(request: Request):
    """Recebe o áudio no corpo da requisição (ex.: Content-Type: audio/wav)."""
    tipo = request.headers.get("content-type", "").split(";")[0].strip().lower()
    formato = FORMATOS_AUDIO.get(tipo)

    if formato is None:
        raise HTTPException(
            status_code=415,
            detail="Formato de áudio não suportado. Envie WAV, MP3, OGG, AAC, AIFF ou FLAC.",
        )

    audio = await request.body()

    if not audio:
        raise HTTPException(status_code=422, detail="O áudio está vazio.")

    if len(audio) > TAMANHO_MAXIMO_AUDIO:
        raise HTTPException(status_code=413, detail="O áudio é muito longo.")

    with erros_da_ia():
        interpretacao = await run_in_threadpool(interpretar_audio, audio, formato)

    if not interpretacao.transcricao.strip():
        raise HTTPException(
            status_code=422,
            detail="Não consegui entender o áudio. Tente falar mais perto do microfone.",
        )

    return {
        "transcricao": interpretacao.transcricao,
        **resultado_da_busca(interpretacao.filtros),
    }
