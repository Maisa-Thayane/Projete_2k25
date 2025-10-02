# plugin.py
from .Banco_Dados.SQlite import banco_bp, init_db
from .Criptografia.Camadas import Criptografia
from .IA import IA
import subprocess, pathlib

class ClinicPlugin:
    def __init__(self, host=None):
        self.host = host
        self.crypto = Criptografia()
        self.ia = IA()

    def integrar(self):
        if self.host:
            # Inicializa banco de dados
            init_db()

            # Registra o blueprint do banco no Flask
            if hasattr(self.host, "register_blueprint"):
                self.host.register_blueprint(banco_bp)

            # Anexa objetos de utilidade ao host
            setattr(self.host, "clinica_crypto", self.crypto)
            setattr(self.host, "clinica_ia", self.ia)

    def abrir_janela(self):
        bat = pathlib.Path(__file__).parent / "executar_janela.bat"
        subprocess.Popen([str(bat)])