from clinica_plugin import ClinicPlugin

# Criar um host qualquer (ou uma instância Flask, se quiser)
class Host:
    pass

host = Host()

# Instanciar o plugin e integrar
plugin = ClinicPlugin(host=host)
plugin.integrar()

# Testar banco de dados: criar usuário
usuario = "cliente_teste"
senha = "123456"

# Criptografa a senha
senha_hash, salt = plugin.crypto.password_hash(senha)

ok = host.clinica_banco.criar_usuario(usuario, senha_hash, salt)
if ok:
    print(f"✅ Usuário '{usuario}' criado com sucesso!")
else:
    print(f"⚠️ Usuário '{usuario}' já existia.")

# Buscar usuário e verificar
user = host.clinica_banco.buscar_usuario(usuario)
if user:
    print(f"✅ Usuário encontrado no banco: {user['username']}")
else:
    print("❌ Não foi possível encontrar o usuário no banco.")

# Testar IA (stub)
resultado_ia = host.clinica_ia.inferir({"evento": "teste"})
print(f"✅ Resultado da IA: {resultado_ia}")

# Testar execução do .bat (opcional)
# plugin.abrir_janela()  # abre a janela local criada