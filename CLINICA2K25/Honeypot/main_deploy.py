from deploy_fake_site import deploy_site

if __name__ == "__main__":
    # Configurações do Cowrie (Notebook B)
    cowrie_host = "192.168.0.5"     # coloque o IP do notebook B
    cowrie_ssh_port = 22             # porta SSH do Cowrie (22 ou 2222 dependendo da config)
    cowrie_user = "Juventino"           # usuário de login no Notebook B
    local_path = "CLINICA2K25"       # pasta do site fake no Notebook A
    http_port = 5007                 # porta onde o site rodará no Notebook B

    deploy_site(
        cowrie_host,
        cowrie_ssh_port,
        cowrie_user,
        local_path,
        http_port
    )
