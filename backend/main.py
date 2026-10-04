from fastapi import FastAPI  # importa o FastAPI
from fastapi.staticfiles import StaticFiles   # ← novo: serve arquivos estáticos (as imagens enviadas)
from fastapi.middleware.cors import CORSMiddleware  # importa o middleware de CORS
from rotas import clientes, senioridade, tatuadores, agendamentos, estilos, usuarios   # ← adiciona estilos aqui
import os   # ← novo: pra criar a pasta de uploads se ela não existir

app = FastAPI()              # cria a aplicação

# Configura quais origens têm permissão de chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # "*" = qualquer origem (usado em desenvolvimento)
    allow_methods=["*"],      # permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],      # permite todos os cabeçalhos
)

os.makedirs("uploads", exist_ok=True)   # garante que a pasta existe antes de tentar servir arquivos dela
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")   # ← serve as imagens

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])  # registra as rotas de clientes na API
app.include_router(senioridade.router, prefix="/senioridade", tags=["Senioridade"])   # ← registra a nova rota
app.include_router(tatuadores.router, prefix="/tatuadores", tags=["Tatuadores"])   # ← registra a nova rota
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])   # ← registra a nova rota
app.include_router(estilos.router, prefix="/estilos", tags=["Estilos"])   # ← registra a nova rota
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])

@app.get("/")                # define que essa função responde ao endereço "/"
def inicio():                # quando alguém acessar "/", essa função vai rodar
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}

