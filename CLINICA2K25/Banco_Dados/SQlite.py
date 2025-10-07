# SQlite.py - Blueprint para sistema de banco de dados
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)
import sqlite3
import re
import os

banco_bp = Blueprint("banco", __name__)


@banco_bp.route("/banco/salvar", methods=["POST"])
def rota_salvar():
    dados = request.json
    return jsonify({"status": "sucesso", "mensagem": "Dados salvos com sucesso!"})


@banco_bp.route("/banco/buscar", methods=["GET"])
def rota_buscar():
    return jsonify({"dados": ["item1", "item2"]})


# Diretório para o banco de dados
# Use o caminho absoluto para o arquivo database.db dentro do diretório da aplicação
# Isso evita que um novo arquivo seja criado no current working directory quando a app
# for iniciada a partir de outra pasta.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATABASE = os.path.join(BASE_DIR, "database.db")


def init_db():
    try:
        if not os.path.exists(DATABASE):
            print("Criando banco de dados...")
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                telefone TEXT
            )
            """
            )

            # Criar usuário admin padrão se não existir
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE email = ?",
                ("admin123@gmail.com.br",),
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, senha, telefone) VALUES (?, ?, ?, ?)",
                    ("admin", "admin123@gmail.com.br", "123456", "(11) 99999-9999"),
                )
                print("Usuário admin padrão criado!")

            conn.commit()
            conn.close()
            print("Banco de dados criado com sucesso!")
        else:
            print("Banco de dados já existe")
    except Exception as e:
        print("Erro ao criar banco de dados:", str(e))


def validar_email(email):
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email)


@banco_bp.route("/api/register", methods=["POST"])
def register():
    try:
        print("Recebendo requisição de registro...")
        data = request.get_json()
        print("Dados recebidos:", data)

        if not data:
            print("Nenhum dado recebido")
            return jsonify({"success": False, "message": "Nenhum dado recebido"}), 400

        nome = data.get("username")
        email = data.get("email")
        senha = data.get("password")
        telefone = data.get("phone", "")

        print(
            f"Dados processados: nome={nome}, email={email}, senha={senha}, telefone={telefone}"
        )

        if not nome or not email or not senha:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Todos os campos obrigatórios devem ser preenchidos",
                    }
                ),
                400,
            )

        if not validar_email(email):
            return (
                jsonify({"success": False, "message": "Formato de email inválido"}),
                400,
            )

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return (
                jsonify({"success": False, "message": "Este email já está cadastrado"}),
                409,
            )

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, telefone) VALUES (?, ?, ?, ?)",
            (nome, email, senha, telefone),
        )
        conn.commit()
        conn.close()

        print("Usuário cadastrado com sucesso!")
        return jsonify({"success": True, "message": "Usuário cadastrado com sucesso!"})

    except Exception as e:
        print("Erro no registro:", str(e))
        return (
            jsonify({"success": False, "message": f"Erro ao cadastrar: {str(e)}"}),
            500,
        )


@banco_bp.route("/api/login", methods=["POST"])
def login():
    try:
        print("Recebendo requisição de login...")
        data = request.get_json()
        print("Dados recebidos:", data)

        if not data:
            return jsonify({"success": False, "message": "Nenhum dado recebido"}), 400

        nome = data.get("username")
        senha = data.get("password")

        if not nome or not senha:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Nome de usuário e senha são obrigatórios",
                    }
                ),
                400,
            )

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha)
        )
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["user_id"] = usuario["id"]
            session["user_name"] = usuario["nome"]

            print("Login bem-sucedido para o usuário:", nome)
            return jsonify(
                {
                    "success": True,
                    "message": "Login realizado com sucesso!",
                    "user": {
                        "id": usuario["id"],
                        "nome": usuario["nome"],
                        "email": usuario["email"],
                    },
                }
            )
        else:
            print("Login falhou para o usuário:", nome)
            return (
                jsonify(
                    {"success": False, "message": "Nome de usuário ou senha incorretos"}
                ),
                401,
            )

    except Exception as e:
        print("Erro no login:", str(e))
        return (
            jsonify({"success": False, "message": f"Erro ao fazer login: {str(e)}"}),
            500,
        )


def processar_login(nome, email, senha, session, max_tentativas=3):
    """
    Função completa para processar login
    Retorna: {'success': bool, 'redirect': str, 'error': str, 'usuario': dict}
    """
    try:
        print(f"Processando login: nome='{nome}', email='{email}'")

        # Verificar tentativas de login
        tentativas = session.get("login_attempts", 0)
        if tentativas >= max_tentativas:
            print(f"Maximo de tentativas excedido: {tentativas}")
            return {
                "success": False,
                "redirect": "second_false",
                "error": None,
                "usuario": None,
            }

        # Conectar ao banco
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Buscar usuário
        cursor.execute(
            "SELECT * FROM usuarios WHERE nome = ? AND email = ? AND senha = ?",
            (nome, email, senha),
        )
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            print(f"Login bem-sucedido: {usuario['nome']}")

            # Limpar tentativas e configurar sessão
            session.pop("login_attempts", None)
            session["user_id"] = usuario["id"]
            session["user_name"] = usuario["nome"]
            session["user_email"] = usuario["email"]

            return {
                "success": True,
                "redirect": "third_page",
                "error": None,
                "usuario": dict(usuario),
            }
        else:
            print(f"Credenciais invalidas")

            # Incrementar tentativas
            session["login_attempts"] = tentativas + 1
            nova_tentativa = session["login_attempts"]

            if nova_tentativa >= max_tentativas:
                print(f"Maximo de tentativas atingido: {nova_tentativa}")
                return {
                    "success": False,
                    "redirect": "second_false",
                    "error": None,
                    "usuario": None,
                }
            else:
                return {
                    "success": False,
                    "redirect": None,
                    "error": "Credenciais inválidas.",
                    "usuario": None,
                }

    except Exception as e:
        print(f"Erro no processamento de login: {str(e)}")
        import traceback

        traceback.print_exc()
        return {
            "success": False,
            "redirect": None,
            "error": f"Erro interno: {str(e)}",
            "usuario": None,
        }


# O módulo de banco de dados agora funciona como blueprint integrado ao app principal
