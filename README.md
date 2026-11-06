# Assistente de Cardápio com IA

API em Python que transforma perguntas em linguagem natural em
filtros para consultar um cardápio fictício. Integra Gemini, valida
respostas com Pydantic e realiza a busca com regras determinísticas
em Python.

Exemplo: “Quero algo vegetariano até 35 reais, sem queijo.”

Projeto pessoal desenvolvido para estudar engenharia de software
e integração de modelos de linguagem.




## Demonstração

Vídeo ilustrado do fluxo de consulta, com exemplo de interpretação
dos filtros, resultado da busca e verificações do projeto.


https://github.com/user-attachments/assets/5daa361d-08a9-4f0f-9101-36f812e1763d





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

- Python: lógica da aplicação e integração dos componentes.
- FastAPI: API HTTP e documentação interativa.
- Gemini 3.1 Flash-Lite: interpretação de perguntas em linguagem natural.
- Pydantic: definição e validação dos filtros.
- Uvicorn: servidor da aplicação.
- unittest e unittest.mock: testes automatizados com simulação da IA.
- Git e GitHub: controle de versões e publicação do código.


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
- `filtros.py`: regras de busca por preço, preferência e ingrediente.
- `main.py`: consulta por filtros pelo terminal.
- `interpretador.py`: integração com Gemini e validação dos filtros.
- `api.py`: rotas de consulta por filtros e linguagem natural.
- `test_filtros.py`: testes das regras de busca.
- `test_api.py`: testes da rota de IA com respostas simuladas.
- `avaliar_ia.py`: avaliação da interpretação com chamadas reais ao Gemini.
- `.env.example`: exemplo de configuração, sem credenciais.
- `requirements.txt`: dependências do projeto.


## Limitações

O filtro de ingredientes consulta apenas os nomes cadastrados.
Ele não verifica alergênicos nem contaminação cruzada.


## Consulta com inteligência artificial

A rota `POST /consultar` usa o Gemini para transformar uma pergunta
em filtros estruturados. O Pydantic valida esses filtros, e o Python
busca os pratos no catálogo fictício.

### Configuração

Copie `.env.example` para `.env` e preencha `GEMINI_API_KEY`
com sua chave do Google AI Studio.

O modelo utilizado é `gemini-3.1-flash-lite`.
A disponibilidade e as cotas dependem da conta do provedor.

### Exemplo de requisição

POST /consultar

```json
{
  "pergunta": "Quero algo vegetariano até 35 reais, sem queijo"
}
```

### Limitações da interpretação

- Pode interpretar perguntas incorretamente.
- Permite excluir apenas um ingrediente por consulta.
- Não possui um filtro específico para pratos veganos.
- Depende da disponibilidade da API externa.
- A validação estrutural não garante que a interpretação esteja correta.

## Avaliação da interpretação com IA

Foi realizada uma avaliação inicial com cinco perguntas e filtros
esperados definidos previamente.

- Modelo: `gemini-3.1-flash-lite`
- Data: 06/11/2026
- Correspondência completa dos filtros: 5/5 casos
- Erros de execução: 0

Os casos incluem preço máximo, preferência vegetariana, exclusão
de ingrediente e consultas sem limite de preço.

Esse resultado representa uma execução de um conjunto pequeno.
Não garante o mesmo desempenho em outras perguntas ou execuções.

Para executar novamente:

```powershell
python avaliar_ia.py
```

A avaliação faz cinco chamadas reais à API e consome sua cota.
Os testes automatizados com `unittest` usam respostas simuladas
na rota de IA.
