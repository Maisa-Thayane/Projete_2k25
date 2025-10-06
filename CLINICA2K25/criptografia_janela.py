import os
import sys
import sqlite3
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox
import queue

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Criptografia.Camadas import criptografar_cinco_camadas, generate_key


class JanelaCriptografia:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema de Criptografia - Clinica 2K25")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2b2b2b")

        # Fila para comunicação entre threads
        self.queue = queue.Queue()

        # Variáveis
        self.resultados = []
        self.chave_publica = ""
        self.chave_privada = ""
        self.executando = False

        self.criar_interface()
        self.verificar_banco()

    def criar_interface(self):
        # Frame principal
        main_frame = Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = Label(
            main_frame,
            text="SISTEMA DE CRIPTOGRAFIA DE DADOS",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#2b2b2b",
        )
        title_label.pack(pady=(0, 20))

        # Frame de controles
        control_frame = Frame(main_frame, bg="#2b2b2b")
        control_frame.pack(fill=X, pady=(0, 10))

        # Botão iniciar
        self.btn_iniciar = Button(
            control_frame,
            text="INICIAR CRIPTOGRAFIA",
            command=self.iniciar_criptografia,
            font=("Arial", 12, "bold"),
            bg="#00aa00",
            fg="white",
            padx=20,
            pady=10,
        )
        self.btn_iniciar.pack(side=LEFT, padx=(0, 10))

        # Botão limpar
        """
        self.btn_limpar = Button(
            control_frame,
            text="LIMPAR",
            command=self.limpar_resultados,
            font=("Arial", 12, "bold"),
            bg="#aa0000",
            fg="white",
            padx=20,
            pady=10,
        )
        self.btn_limpar.pack(side=LEFT, padx=(0, 10))
        """

        # Status
        self.status_label = Label(
            control_frame,
            text="Pronto para iniciar",
            font=("Arial", 10),
            fg="#ffff00",
            bg="#2b2b2b",
        )
        self.status_label.pack(side=LEFT, padx=(20, 0))

        # Frame de progresso
        progress_frame = Frame(main_frame, bg="#2b2b2b")
        progress_frame.pack(fill=X, pady=(0, 10))

        # Barra de progresso
        self.progress = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress.pack(fill=X)

        # Frame de conteúdo
        content_frame = Frame(main_frame, bg="#2b2b2b")
        content_frame.pack(fill=BOTH, expand=True)

        # Notebook para abas
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        # Configurar estilo escuro para o notebook
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar cores escuras para as abas
        style.configure("TNotebook", background="#2b2b2b", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#404040",
            foreground="#ffffff",
            padding=[20, 10],
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab", background=[("selected", "#1e1e1e"), ("active", "#505050")]
        )

        # Configurar estilo escuro para as treeviews
        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="#ffffff",
            fieldbackground="#1e1e1e",
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background="#404040",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map("Treeview.Heading", background=[("active", "#505050")])

        # Configurar estilo escuro para a barra de progresso
        style.configure(
            "TProgressbar", background="#00aa00", troughcolor="#404040", borderwidth=0
        )

        # Aba de log
        self.log_frame = Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.log_frame, text="Log de Execução")

        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00", wrap=WORD
        )
        self.log_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Aba de resultados originais
        self.result_frame = Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.result_frame, text="Dados Originais")

        # Treeview para dados originais
        columns_orig = (
            "ID",
            "Nome",
            "Email",
            "Senha",
            "Expansão Nome",
            "Expansão Email",
            "Expansão Senha",
        )
        self.tree_orig = ttk.Treeview(
            self.result_frame, columns=columns_orig, show="headings"
        )

        # Configurar colunas
        for col in columns_orig:
            self.tree_orig.heading(col, text=col)
            self.tree_orig.column(col, width=120)

        # Scrollbar para treeview original
        tree_scroll_orig = ttk.Scrollbar(
            self.result_frame, orient=VERTICAL, command=self.tree_orig.yview
        )
        self.tree_orig.configure(yscrollcommand=tree_scroll_orig.set)

        self.tree_orig.pack(side=LEFT, fill=BOTH, expand=True)
        tree_scroll_orig.pack(side=RIGHT, fill=Y)

        # Aba de dados criptografados
        self.cript_frame = Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.cript_frame, text="Dados Criptografados")

        # Treeview para dados criptografados
        columns_cript = (
            "ID",
            "Nome Criptografado",
            "Email Criptografado",
            "Senha Criptografada",
            "Tamanho Nome",
            "Tamanho Email",
            "Tamanho Senha",
        )
        self.tree_cript = ttk.Treeview(
            self.cript_frame, columns=columns_cript, show="headings"
        )

        # Configurar colunas
        for col in columns_cript:
            self.tree_cript.heading(col, text=col)
            if col == "ID":
                self.tree_cript.column(col, width=50)
            elif "Criptografado" in col:
                self.tree_cript.column(col, width=200)
            else:
                self.tree_cript.column(col, width=100)

        # Scrollbar para treeview criptografado
        tree_scroll_cript = ttk.Scrollbar(
            self.cript_frame, orient=VERTICAL, command=self.tree_cript.yview
        )
        self.tree_cript.configure(yscrollcommand=tree_scroll_cript.set)

        self.tree_cript.pack(side=LEFT, fill=BOTH, expand=True)
        tree_scroll_cript.pack(side=RIGHT, fill=Y)

        # Aba de chaves
        self.keys_frame = Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.keys_frame, text="Chaves de Criptografia")

        # Texto para chaves
        self.keys_text = scrolledtext.ScrolledText(
            self.keys_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#ffff00",
            wrap=WORD,
        )
        self.keys_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

    def verificar_banco(self):
        """Verifica se o banco de dados existe"""
        if not os.path.exists("database.db"):
            self.log("ERRO: Banco de dados 'database.db' não encontrado!")
            self.status_label.config(text="Erro: Banco não encontrado", fg="#ff0000")
            self.btn_iniciar.config(state=DISABLED)
        else:
            self.log("Banco de dados encontrado: database.db")
            self.status_label.config(text="Pronto para iniciar", fg="#ffff00")

    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(END, f"[{timestamp}] {mensagem}\n")
        self.log_text.see(END)
        self.root.update_idletasks()

    def iniciar_criptografia(self):
        # Evitar cliques duplicados
        if self.executando:
            return

        # Limpar resultados anteriores
        self.limpar_resultados()

        """Inicia o processo de criptografia em thread separada"""
        self.executando = True
        self.btn_iniciar.config(state=DISABLED)
        self.progress.start()
        self.status_label.config(text="Executando criptografia...", fg="#ffff00")

        # Iniciar thread de criptografia
        thread = threading.Thread(target=self.executar_criptografia)
        thread.daemon = True
        thread.start()

        # Iniciar verificação de queue
        self.root.after(100, self.verificar_queue)

    def executar_criptografia(self):
        """Executa a criptografia dos dados"""
        try:
            self.queue.put(("log", "Iniciando processo de criptografia..."))

            # Gerar chaves ECC
            self.queue.put(("log", "Gerando chaves ECC..."))
            chave_privada = generate_key()
            self.chave_privada = chave_privada.secret.hex()
            self.chave_publica = chave_privada.public_key.format().hex()

            self.queue.put(("log", f"Chave Publica ECC: {self.chave_publica}"))
            # self.queue.put(("log", f"Chave Privada ECC: {self.chave_privada}"))

            # Conectar ao banco
            self.queue.put(("log", "Conectando ao banco de dados..."))
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, email, senha, telefone FROM usuarios")
            usuarios = cursor.fetchall()
            conn.close()

            self.queue.put(("log", f"Encontrados {len(usuarios)} usuarios no banco"))

            if len(usuarios) == 0:
                self.queue.put(("log", "AVISO: Nenhum usuario encontrado!"))
                self.queue.put(("status", "Nenhum usuario encontrado"))
                return

            # Processar cada usuário
            self.queue.put(("log", "Iniciando criptografia dos dados..."))

            for i, usuario in enumerate(usuarios, 1):
                self.queue.put(
                    (
                        "log",
                        f"[{i}/{len(usuarios)}] Processando usuario ID {usuario['id']}",
                    )
                )
                self.queue.put(("log", f"   Nome: {usuario['nome']}"))
                self.queue.put(("log", f"   Email: {usuario['email']}"))
                self.queue.put(("log", f"   Senha: {'*' * len(usuario['senha'])}"))

                try:
                    # Criptografar campos
                    self.queue.put(("log", "   Criptografando campos..."))

                    nome_cript = criptografar_cinco_camadas(
                        self.chave_publica, usuario["nome"]
                    )
                    email_cript = criptografar_cinco_camadas(
                        self.chave_publica, usuario["email"]
                    )
                    senha_cript = criptografar_cinco_camadas(
                        self.chave_publica, usuario["senha"]
                    )

                    # Calcular taxas de expansão
                    taxa_nome = len(nome_cript) / len(usuario["nome"])
                    taxa_email = len(email_cript) / len(usuario["email"])
                    taxa_senha = len(senha_cript) / len(usuario["senha"])

                    self.queue.put(("log", f"   RESULTADOS:"))
                    self.queue.put(
                        (
                            "log",
                            f"      Nome: {len(usuario['nome'])} -> {len(nome_cript)} chars (expansao: {taxa_nome:.2f}x)",
                        )
                    )
                    self.queue.put(
                        (
                            "log",
                            f"      Email: {len(usuario['email'])} -> {len(email_cript)} chars (expansao: {taxa_email:.2f}x)",
                        )
                    )
                    self.queue.put(
                        (
                            "log",
                            f"      Senha: {len(usuario['senha'])} -> {len(senha_cript)} chars (expansao: {taxa_senha:.2f}x)",
                        )
                    )

                    # Adicionar aos resultados
                    resultado = {
                        "id": usuario["id"],
                        "nome": usuario["nome"],
                        "email": usuario["email"],
                        "senha": usuario["senha"],
                        "taxa_nome": taxa_nome,
                        "taxa_email": taxa_email,
                        "taxa_senha": taxa_senha,
                        "nome_cript": nome_cript,
                        "email_cript": email_cript,
                        "senha_cript": senha_cript,
                    }
                    self.queue.put(("resultado", resultado))

                    self.queue.put(
                        (
                            "log",
                            f"   Usuario {usuario['id']} criptografado com sucesso!",
                        )
                    )

                except Exception as e:
                    self.queue.put(
                        ("log", f"   ERRO no usuario {usuario['id']}: {str(e)}")
                    )

            # Finalizar
            self.queue.put(("log", "Criptografia concluida com sucesso!"))
            self.queue.put(("status", "Criptografia concluida"))
            self.queue.put(("chaves", (self.chave_publica, self.chave_privada)))

        except Exception as e:
            self.queue.put(("log", f"ERRO GERAL: {str(e)}"))
            self.queue.put(("status", "Erro na criptografia"))

    def verificar_queue(self):
        """Verifica mensagens da queue e atualiza interface"""
        try:
            while True:
                tipo, dados = self.queue.get_nowait()

                if tipo == "log":
                    self.log(dados)
                elif tipo == "status":
                    self.status_label.config(
                        text=dados,
                        fg="#00ff00" if "concluida" in dados.lower() else "#ff0000",
                    )
                    # Parar quando concluir ou houver erro
                    if "concluida" in dados.lower() or "erro" in dados.lower():
                        self.executando = False
                        try:
                            self.progress.stop()
                        except Exception:
                            pass
                elif tipo == "resultado":
                    self.adicionar_resultado(dados)
                elif tipo == "chaves":
                    self.mostrar_chaves(dados[0], dados[1])

        except queue.Empty:
            pass

        # Continuar verificando enquanto estiver executando
        if self.executando:
            self.root.after(100, self.verificar_queue)
        else:
            self.btn_iniciar.config(state=NORMAL)

    def adicionar_resultado(self, resultado):
        """Adiciona resultado às tabelas"""
        # Adicionar à tabela de dados originais
        self.tree_orig.insert(
            "",
            "end",
            values=(
                resultado["id"],
                resultado["nome"],
                resultado["email"],
                resultado["senha"],
                f"{resultado['taxa_nome']:.2f}x",
                f"{resultado['taxa_email']:.2f}x",
                f"{resultado['taxa_senha']:.2f}x",
            ),
        )

        # Adicionar à tabela de dados criptografados
        self.tree_cript.insert(
            "",
            "end",
            values=(
                resultado["id"],
                (
                    resultado["nome_cript"][:100] + "..."
                    if len(resultado["nome_cript"]) > 100
                    else resultado["nome_cript"]
                ),
                (
                    resultado["email_cript"][:100] + "..."
                    if len(resultado["email_cript"]) > 100
                    else resultado["email_cript"]
                ),
                (
                    resultado["senha_cript"][:100] + "..."
                    if len(resultado["senha_cript"]) > 100
                    else resultado["senha_cript"]
                ),
                len(resultado["nome_cript"]),
                len(resultado["email_cript"]),
                len(resultado["senha_cript"]),
            ),
        )

    def mostrar_chaves(self, chave_publica, chave_privada):
        """Mostra as chaves de criptografia"""
        self.keys_text.delete(1.0, END)
        self.keys_text.insert(END, "CHAVES DE CRIPTOGRAFIA ECC\n")
        self.keys_text.insert(END, "=" * 50 + "\n\n")
        self.keys_text.insert(END, f"Chave Publica:\n{chave_publica}\n\n")
        self.keys_text.insert(END, f"Chave Privada:\n{chave_privada}\n\n")
        self.keys_text.insert(END, "IMPORTANTE:\n")
        self.keys_text.insert(END, "- Mantenha a chave privada em local seguro!\n")
        self.keys_text.insert(
            END, "- A chave privada e necessaria para descriptografar os dados!\n"
        )
        self.keys_text.insert(
            END, "- Os dados foram criptografados com 5 camadas de seguranca!\n"
        )

    def limpar_resultados(self):
        """Limpa todos os resultados"""
        self.log_text.delete(1.0, END)
        self.tree_orig.delete(*self.tree_orig.get_children())
        self.tree_cript.delete(*self.tree_cript.get_children())
        self.keys_text.delete(1.0, END)
        self.resultados = []

    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    app = JanelaCriptografia()
    app.executar()
