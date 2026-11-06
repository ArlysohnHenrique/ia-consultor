# Assistente de Cardápio

Projeto de estudo em Python para consultar um cardápio fictício por
preço, preferência vegetariana e ingrediente que se deseja evitar.

## Funcionalidades

- Consulta pelo terminal.
- API HTTP com FastAPI.
- Filtro por preço máximo.
- Filtro de pratos vegetarianos.
- Exclusão de ingredientes por busca textual.
- Testes automatizados com unittest.

## Tecnologias

Python, FastAPI, Uvicorn e unittest.

## Como executar

Os comandos abaixo são para Windows PowerShell.

### 1. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 2. Instalar as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Executar pelo terminal

```powershell
.\.venv\Scripts\python.exe main.py
```

### 4. Iniciar a API

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

Acesse a documentação interativa em:
http://127.0.0.1:8000/docs

Exemplo de consulta:
http://127.0.0.1:8000/pratos?preco_maximo=30

Para encerrar o servidor, pressione Ctrl+C.

## Executar os testes

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Organização

- `dados.py`: catálogo fictício de pratos.
- `filtros.py`: regras de busca.
- `main.py`: interação pelo terminal.
- `api.py`: rotas HTTP.
- `test_filtros.py`: testes dos filtros.

## Limitações

O filtro de ingredientes consulta apenas os nomes cadastrados.
Ele não verifica alergênicos nem contaminação cruzada.

## Próximos passos

- Integrar um LLM para interpretar perguntas em linguagem natural.
- Validar os filtros extraídos pelo modelo.
- Avaliar a qualidade das respostas.