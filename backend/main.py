from fastapi import FastAPI, Depends  # importa o FastAPI
from fastapi.staticfiles import StaticFiles   # ← novo: serve arquivos estáticos (as imagens enviadas)
from fastapi.middleware.cors import CORSMiddleware  # importa o middleware de CORS
from rotas import clientes, senioridade, tatuadores, agendamentos, estilos, usuarios, login   # ← adiciona estilos aqui
from seguranca import verificar_token, verificar_admin
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

app.include_router(login.router, tags=["Login"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"], dependencies=[Depends(verificar_admin)])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verificar_token)])  # registra as rotas de clientes na API
app.include_router(senioridade.router, prefix="/senioridade", tags=["Senioridade"], dependencies=[Depends(verificar_token)])   # ← registra a nova rota
app.include_router(estilos.router, prefix="/estilos", tags=["Estilos"], dependencies=[Depends(verificar_token)])   # ← registra a nova rota
app.include_router(tatuadores.router, prefix="/tatuadores", tags=["Tatuadores"], dependencies=[Depends(verificar_token)])   # ← registra a nova rota
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"], dependencies=[Depends(verificar_token)])   # ← registra a nova rota




@app.get("/")                # define que essa função responde ao endereço "/"
def inicio():                # quando alguém acessar "/", essa função vai rodar
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}

