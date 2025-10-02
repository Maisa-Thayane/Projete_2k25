import paramiko
import os

def deploy_site(cowrie_host, cowrie_ssh_port, cowrie_user, local_path, http_port):
    """
    Faz deploy do fake site no Notebook B (Cowrie).
    - Envia arquivos via SFTP.
    - Inicia um servidor HTTP na porta definida.
    """
    try:
        # Criar conexão SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cowrie_host, port=cowrie_ssh_port, username=cowrie_user)

        # Criar sessão SFTP
        sftp = ssh.open_sftp()
        remote_dir = f"/home/{cowrie_user}/fake_site"

        try:
            sftp.mkdir(remote_dir)
        except IOError:
            pass  # já existe

        # Enviar arquivos
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_dir, file)
                sftp.put(local_file, remote_file)

        sftp.close()

        # Iniciar servidor HTTP no Cowrie (Notebook B)
        command = f"nohup python3 -m http.server {http_port} --directory {remote_dir} >/dev/null 2>&1 &"
        ssh.exec_command(command)

        ssh.close()
        print(f"✅ Página falsa servida no Cowrie em http://{cowrie_host}:{http_port}")

    except Exception as e:
        print(f"❌ Erro no deploy: {e}")
