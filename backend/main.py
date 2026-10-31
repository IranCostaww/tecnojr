import os
import sqlite3
from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

app = FastAPI(title="API Encomendas Cafe do Bairro")

# liberando o cors pro front em html conseguir chamar a api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# caminho para o banco sqlite ficar sempre na mesma pasta deste arquivo
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO = os.environ.get("BANCO_ENCOMENDAS", "encomendas.db")
CAMINHO_BANCO = os.path.join(PASTA_ATUAL, NOME_BANCO)

STATUS_PERMITIDOS = ["recebida", "em preparo", "entregue"]
LIMITE_POR_DIA = 5

# funcao simples pra conectar no sqlite e trazer os resultados como dicionario
def pegar_conexao():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row
    return conn

# cria a tabela logo que o arquivo sobe se ela ainda nao existir
def iniciar_banco():
    conn = pegar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encomendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            produto TEXT NOT NULL,
            data_entrega TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'recebida'
        )
    """)
    conn.commit()
    conn.close()

iniciar_banco()

# modelos para validar o que chega no corpo da requisicao
class EncomendaCriar(BaseModel):
    cliente_nome: str
    telefone: str
    produto: str
    data_entrega: date
    status: Optional[str] = "recebida"

    # valida se o telefone tem apenas digitos e entre 10 e 11 caracteres
    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, v: str) -> str:
        if not v.isdigit() or len(v) not in (10, 11):
            raise ValueError("O telefone deve conter apenas digitos, entre 10 e 11 caracteres.")
        return v

class EncomendaAtualizar(BaseModel):
    cliente_nome: Optional[str] = None
    telefone: Optional[str] = None
    produto: Optional[str] = None
    data_entrega: Optional[date] = None
    status: Optional[str] = None

    # se enviou telefone na atualizacao, aplica a mesma regra de digitos
    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.isdigit() or len(v) not in (10, 11):
                raise ValueError("O telefone deve conter apenas digitos, entre 10 e 11 caracteres.")
        return v

# rota para cadastrar uma nova encomenda
@app.post("/encomendas", status_code=status.HTTP_201_CREATED)
def criar_encomenda(dados: EncomendaCriar):
    conn = pegar_conexao()
    cursor = conn.cursor()

    # valida se o status enviado e um dos tres permitidos
    status_limpo = dados.status.lower().strip() if dados.status else "recebida"
    if status_limpo not in STATUS_PERMITIDOS:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Status invalido. Escolha: recebida, em preparo ou entregue."
        )

    # bloqueia encomendas com data no passado
    if dados.data_entrega < date.today():
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="A data de entrega nao pode ser no passado."
        )

    # padroniza a data para texto no formato AAAA-MM-DD
    data_texto = dados.data_entrega.isoformat()

    # aqui eu conto quantas encomendas ja tem no dia
    cursor.execute(
        "SELECT COUNT(*) FROM encomendas WHERE data_entrega = ?",
        (data_texto,)
    )
    total_no_dia = cursor.fetchone()[0]

    # se passou ou atingiu o limite de 5 devolve erro
    if total_no_dia >= LIMITE_POR_DIA:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Limite de 5 encomendas atingido para este dia. Escolha outra data."
        )

    cursor.execute(
        """
        INSERT INTO encomendas (cliente_nome, telefone, produto, data_entrega, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (dados.cliente_nome, dados.telefone, dados.produto, data_texto, status_limpo)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return {
        "id": novo_id,
        "cliente_nome": dados.cliente_nome,
        "telefone": dados.telefone,
        "produto": dados.produto,
        "data_entrega": data_texto,
        "status": status_limpo
    }

# essa aqui e a funcao que lista as encomendas, com filtro opcional de data
@app.get("/encomendas")
def listar_encomendas(data: Optional[date] = None):
    conn = pegar_conexao()
    cursor = conn.cursor()

    if data:
        data_texto = data.isoformat()
        cursor.execute("SELECT * FROM encomendas WHERE data_entrega = ? ORDER BY id DESC", (data_texto,))
    else:
        cursor.execute("SELECT * FROM encomendas ORDER BY data_entrega ASC, id DESC")

    linhas = cursor.fetchall()
    conn.close()

    resultado = []
    for linha in linhas:
        resultado.append(dict(linha))

    return resultado

# rota para pegar uma encomenda especifica pelo id
@app.get("/encomendas/{encomenda_id}")
def buscar_encomenda(encomenda_id: int):
    conn = pegar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encomendas WHERE id = ?", (encomenda_id,))
    linha = cursor.fetchone()
    conn.close()

    if not linha:
        raise HTTPException(status_code=404, detail="Encomenda nao encontrada.")

    return dict(linha)

# rota para atualizar dados ou status de uma encomenda
@app.put("/encomendas/{encomenda_id}")
def atualizar_encomenda(encomenda_id: int, dados: EncomendaAtualizar):
    conn = pegar_conexao()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM encomendas WHERE id = ?", (encomenda_id,))
    encomenda_atual = cursor.fetchone()

    if not encomenda_atual:
        conn.close()
        raise HTTPException(status_code=404, detail="Encomenda nao encontrada.")

    encomenda_atual_dict = dict(encomenda_atual)

    # se enviou status, valida se e valido
    novo_status = encomenda_atual_dict["status"]
    if dados.status is not None:
        status_limpo = dados.status.lower().strip()
        if status_limpo not in STATUS_PERMITIDOS:
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Status invalido. Escolha: recebida, em preparo ou entregue."
            )
        novo_status = status_limpo

    # se trocou a data de entrega, precisa verificar o limite do novo dia e impedir passado
    nova_data = encomenda_atual_dict["data_entrega"]
    if dados.data_entrega is not None:
        if dados.data_entrega < date.today():
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="A data de entrega nao pode ser no passado."
            )
        data_alterada = dados.data_entrega.isoformat()
        if data_alterada != encomenda_atual_dict["data_entrega"]:
            cursor.execute(
                "SELECT COUNT(*) FROM encomendas WHERE data_entrega = ? AND id != ?",
                (data_alterada, encomenda_id)
            )
            total_novo_dia = cursor.fetchone()[0]
            if total_novo_dia >= LIMITE_POR_DIA:
                conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="Limite de 5 encomendas atingido para este dia. Escolha outra data."
                )
            nova_data = data_alterada

    novo_nome = dados.cliente_nome if dados.cliente_nome is not None else encomenda_atual_dict["cliente_nome"]
    novo_telefone = dados.telefone if dados.telefone is not None else encomenda_atual_dict["telefone"]
    novo_produto = dados.produto if dados.produto is not None else encomenda_atual_dict["produto"]

    cursor.execute(
        """
        UPDATE encomendas
        SET cliente_nome = ?, telefone = ?, produto = ?, data_entrega = ?, status = ?
        WHERE id = ?
        """,
        (novo_nome, novo_telefone, novo_produto, nova_data, novo_status, encomenda_id)
    )
    conn.commit()
    conn.close()

    return {
        "id": encomenda_id,
        "cliente_nome": novo_nome,
        "telefone": novo_telefone,
        "produto": novo_produto,
        "data_entrega": nova_data,
        "status": novo_status
    }

# rota para remover uma encomenda
@app.delete("/encomendas/{encomenda_id}")
def remover_encomenda(encomenda_id: int):
    conn = pegar_conexao()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM encomendas WHERE id = ?", (encomenda_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Encomenda nao encontrada.")

    cursor.execute("DELETE FROM encomendas WHERE id = ?", (encomenda_id,))
    conn.commit()
    conn.close()

    return {"mensagem": "Encomenda removida com sucesso."}
