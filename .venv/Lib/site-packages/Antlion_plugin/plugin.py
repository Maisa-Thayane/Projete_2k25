# plugin.py
from .Banco_Dados.SQlite import banco_bp, init_db
from .IA import analisar_comportamento
from .Criptografia.Camadas import criptografar_cinco_camadas


class AntlionPlugin:
    def __init__(self, host=None):
        self.host = host

    def integrar(self):
        if self.host:
            # Inicializa banco de dados
            init_db()

            # Registra o blueprint do banco no Flask
            if hasattr(self.host, "register_blueprint"):
                self.host.register_blueprint(banco_bp, url_prefix="/banco")

            # Anexa suas funções existentes ao host
            setattr(self.host, "clinica_ia", analisar_comportamento)
            setattr(self.host, "clinica_crypto", criptografar_cinco_camadas)
