from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import os, requests, subprocess, random
from flask_mail import Mail, Message
#from Honeypot.deploy_fake_site import deploy_via_sftp
import smtplib
import email.message

from IA import ia_bp # Importa o blueprint da IA
from Banco_Dados.SQlite import (
 banco_bp,
 init_db,
 processar_login,
) # Importa o blueprint do banco de dados e funções


app = Flask(__name__)
CORS(
 app, resources={r"/*": {"origins": "*"}}
) # Configura CORS para permitir requisições

def enviar_codigo_email(email_destinatario, codigo):
 # Cria uma mensagem de e-mail
    msg = Message('Seu código de verificação',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email_destinatario])
    msg.body = f'Olá, aqui está seu código de verificação de 4 dígitos: {codigo}. Use-o para acessar sua conta.'
    try:
        mail.send(msg)
        print(f"E-mail enviado para {email_destinatario} com o código: {codigo}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        # Lógica de fallback ou log de erro pode ser adicionada aqui

# Configurações do servidor de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'antlion2K25@gmail.com'
app.config['MAIL_PASSWORD'] = 'oqrlttaveqjixcib'

mail = Mail(app)


# Registra os blueprints com prefixos apropriados
app.register_blueprint(ia_bp, url_prefix="/ia")
app.register_blueprint(banco_bp, url_prefix="/banco")

app.secret_key = os.urandom(24)

# --- Configurações do Site (Regras) ---
MAX_TENTATIVAS = 1
ABUSEIPDB_API_KEY = (
 "f8648e37c4b82a8f8232a29bc9e9c519421c6c2db71b743c7531e22422dc43925caa857c4e67831a"
)
RECAPTCHA_SECRET_KEY = "6Ld0EWgrAAAAAMEfW1hruoOELH9ViJX522cVpNrC"


# ------------------- ROTAS (PÁGINAS DO SITE) -------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/second", methods=["GET", "POST"])
def second():
    # Limpa as tentativas de login quando a página é acessada via GET
    if request.method == "GET":
        session["login_attempts"] = 0
        session.pop("honeypot_activated", None)

    if session.get("login_attempts", 0) >= MAX_TENTATIVAS:
        ip = request.remote_addr
        redirecionar_para_cowrie(ip)
        session["honeypot_activated"] = True
        return redirect("http://192.168.0.5") #P/ Davi

    def redirecionar_para_cowrie(ip):
        regra = [
            "iptables", "-t", "nat", "-A", "PREROUTING",
            "-s", ip, "-p", "tcp", "--dport", "5007",
            "-j", "REDIRECT", "--to-port", "2222"
        ]
        subprocess.run(regra)

        
        return render_template("second.html")
        

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        behavioral_data_json = request.form.get("behavioral_data", "{}")
        resultado_login = processar_login(nome, email, senha, session, MAX_TENTATIVAS)
        try:
            import json
            behavioral_data = json.loads(behavioral_data_json)
            print(
                f"Dados comportamentais recebidos: {len(behavioral_data.get('mouse_movements', []))} movimentos, {len(behavioral_data.get('key_press_times', []))} teclas, {len(behavioral_data.get('click_events', []))} cliques"
            )
        except:
            behavioral_data = {
                "mouse_movements": [],
                "key_press_times": [],
                "click_events": [],
            }
            print("Erro ao processar dados comportamentais, usando dados vazios")

        if not nome or not email or not senha:
            return render_template("second.html", error="Preencha todos os campos.")

        recaptcha_response = request.form.get("g-recaptcha-response")
        verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response},
        )
        resultado = verify.json()
        if not resultado.get("success"):
            return render_template(
                "second.html",
                error="Falha na verificação do reCAPTCHA. Tente novamente.",
            )

        try:
            ip = request.remote_addr
            headers = {"Accept": "application/json", "Key": ABUSEIPDB_API_KEY}
            params = {"ipAddress": ip, "maxAgeInDays": 90}
            response = requests.get(
                "https://api.abuseipdb.com/api/v2/check", headers=headers, params=params
            )
            score = response.json()["data"]["abuseConfidenceScore"]
            #score = 60; /Teste local
            if score > 20:
                return redirect("http://192.168.0.5")
        except Exception as e:
            return render_template(
                "second.html", error=f"Erro ao verificar IP: {str(e)}"
            )

        resultado_login = processar_login(nome, email, senha, session, MAX_TENTATIVAS)

        if resultado_login["success"]:
            try:
                from IA import analisar_comportamento
                print("Analisando dados comportamentais reais...")
                resultado_ia = analisar_comportamento(behavioral_data)
                print(f"Resultado da IA: {resultado_ia}")
            except Exception as ia_error:
                print(f"Erro na IA (continuando login): {str(ia_error)}")
            
            # Armazena o e-mail do usuário na sessão para uso posterior
            session['user_email'] = email
            
            return redirect(url_for(resultado_login["redirect"]))

        elif resultado_login["redirect"]:
            return redirect(url_for(resultado_login["redirect"]))

        else:
            return render_template("second.html", error=resultado_login["error"])

    return render_template("second.html")

@app.route("/secondfalse")
def second_false():
    return redirect("http://192.168.0.5")


@app.route('/gerar-e-enviar-codigo')
def gerar_e_enviar_codigo():
    codigo_verificacao = random.randint(1000, 9999)
    session['verification_code'] = codigo_verificacao
    
    email_do_usuario = session.get('user_email')

    if email_do_usuario:
        enviar_codigo_email(email_do_usuario, codigo_verificacao)
    
    return redirect(url_for('third_page'))

 
@app.route('/third')
def third_page():
    # Verifica se o código foi gerado; se não, redireciona para gerar.
    if 'verification_code' not in session:
        return redirect(url_for('gerar_e_enviar_codigo'))
    return render_template('third.html')


@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    user_code = data.get('code', None)
    
    # A verificação é feita em uma única tentativa. Se falhar, o código é invalidado.
    correct_code = session.pop('verification_code', None)

    if not user_code or not correct_code:
        return jsonify(success=False, error="Sessão expirada ou código inválido. Tente fazer o login novamente.")

    try:
        user_code_int = int(user_code)
        
        if user_code_int == correct_code:
            return jsonify(success=True, redirect_url=url_for('fourth_page'))
        else:
            return jsonify(success=False, error="Código incorreto. Tente novamente.")
    except ValueError:
        return jsonify(success=False, error="Entrada inválida. Por favor, digite apenas números.")


@app.route("/fourth")
def fourth_page():
    return render_template("fourth.html")


if __name__ == "__main__":
    print("Inicializando banco de dados...")
    try:
        init_db()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 50)
    print("SISTEMA CLÍNICA 2K25 INICIADO")
    print("=" * 50)
    print("Servidor principal: http://localhost:5007")
    print("Página de cadastro: http://localhost:5007/cadastro")
    print("Página de login: http://localhost:5007/second")
    print("=" * 50)
    print("Os prints da IA aparecerão aqui no console principal!")
    print("=" * 50)

    app.run(debug=True, port=5007)