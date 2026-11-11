import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

MODELO_PADRAO = "gemini-3.1-flash-lite"


class ConfiguracaoAusenteError(RuntimeError):
    """Uma variável de ambiente obrigatória não foi definida."""


@dataclass(frozen=True)
class Configuracao:
    gemini_api_key: str
    gemini_model: str = MODELO_PADRAO


@lru_cache
def carregar_configuracao() -> Configuracao:
    """Lê o .env uma única vez e valida as variáveis obrigatórias."""
    load_dotenv(Path(__file__).with_name(".env"))

    chave = os.getenv("GEMINI_API_KEY", "").strip()
    if not chave:
        raise ConfiguracaoAusenteError("Configure GEMINI_API_KEY no arquivo .env.")

    return Configuracao(
        gemini_api_key=chave,
        gemini_model=os.getenv("GEMINI_MODEL", "").strip() or MODELO_PADRAO,
    )
