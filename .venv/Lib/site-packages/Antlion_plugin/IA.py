from flask import Blueprint, request, jsonify
from flask_cors import CORS

ia_bp = Blueprint("ia", __name__)


@ia_bp.route("/ia", methods=["POST"])
def rota_ia():
    dados = request.json
    return jsonify({"resultado": f"IA processou: {dados['entrada']}"})


@ia_bp.route("/behavioral_data", methods=["POST"])
def behavioral_data():
    data = request.json
    print("Received behavioral data:", data)

    # --- Início da Lógica de Detecção da IA --- //
    # Inicializa o score de risco
    risk_score = 0.0

    # Extrai os dados comportamentais do JSON recebido
    mouse_movements = data.get("mouse_movements", [])
    key_press_times = data.get("key_press_times", [])
    click_events = data.get("click_events", [])

    # Heurística 1: Analisa movimentos do mouse
    # Bots tendem a ter poucos ou movimentos muito padronizados
    if len(mouse_movements) < 10:  # Pouquíssimos movimentos do mouse
        risk_score += 0.3
    elif len(mouse_movements) < 50:  # Poucos movimentos do mouse
        risk_score += 0.1

    # Heurística 2: Analisa tempos de pressionamento de tecla (velocidade e consistência da digitação)
    # Bots geralmente digitam em velocidades muito rápidas e uniformes
    if len(key_press_times) > 1:
        time_diffs = []
        for i in range(1, len(key_press_times)):
            # Calcula a diferença de tempo entre os pressionamentos de tecla
            time_diffs.append(
                key_press_times[i]["time"] - key_press_times[i - 1]["time"]
            )

        if time_diffs:
            avg_time_diff = sum(time_diffs) / len(time_diffs)
            # Se a digitação for muito rápida (ex: menos de 50ms por tecla) ou muito uniforme
            if avg_time_diff < 50 or (
                len(time_diffs) > 5 and max(time_diffs) - min(time_diffs) < 200
            ):
                risk_score += 0.4

    # Heurística 3: Analisa eventos de clique
    # Bots tendem a ter poucos cliques ou cliques em locais muito específicos
    if len(click_events) < 2:  # Pouquíssimos cliques
        risk_score += 0.2

    # Define um limiar de suspeita. Este valor foi reduzido para facilitar os testes.
    suspicion_threshold = 0.1
    is_suspicious = (
        risk_score > suspicion_threshold
    )  # Verifica se o score de risco ultrapassa o limiar

    # --- Fim da Lógica de Detecção da IA --- //

    # Retorna a decisão da IA para o frontend
    if is_suspicious:
        response_data = {
            "status": "suspicious",
            "message": "Atividade incomum detectada. Por favor, complete uma verificação extra.",
        }
        print(
            f"Resposta da IA: {response_data}"
        )  # Imprime a resposta no terminal do servidor da IA para depuração
        return jsonify(response_data)
    else:
        response_data = {"status": "ok", "message": "Login permitido."}
        print(
            f"Resposta da IA: {response_data}"
        )  # Imprime a resposta no terminal do servidor da IA para depuração
        return jsonify(response_data)


# Função para chamar a IA diretamente (sem precisar de request)
def analisar_comportamento(dados_comportamentais):
    """
    Função para analisar dados comportamentais diretamente
    Retorna o resultado da análise da IA
    """
    print("=" * 50)
    print("ANÁLISE COMPORTAMENTAL DA IA")
    print("=" * 50)
    print("Dados recebidos:", dados_comportamentais)

    # Inicializa o score de risco
    risk_score = 0.0

    # Extrai os dados comportamentais
    mouse_movements = dados_comportamentais.get("mouse_movements", [])
    key_press_times = dados_comportamentais.get("key_press_times", [])
    click_events = dados_comportamentais.get("click_events", [])

    # Heurística 1: Analisa movimentos do mouse
    if len(mouse_movements) < 10:
        risk_score += 0.3
    elif len(mouse_movements) < 50:
        risk_score += 0.1

    # Heurística 2: Analisa tempos de pressionamento de tecla
    if len(key_press_times) > 1:
        time_diffs = []
        for i in range(1, len(key_press_times)):
            time_diffs.append(
                key_press_times[i]["time"] - key_press_times[i - 1]["time"]
            )

        if time_diffs:
            avg_time_diff = sum(time_diffs) / len(time_diffs)
            if avg_time_diff < 50 or (
                len(time_diffs) > 5 and max(time_diffs) - min(time_diffs) < 200
            ):
                risk_score += 0.4

    # Heurística 3: Analisa eventos de clique
    if len(click_events) < 2:
        risk_score += 0.2

    # Define um limiar de suspeita
    suspicion_threshold = 0.1
    is_suspicious = risk_score > suspicion_threshold

    # Retorna a decisão da IA
    if is_suspicious:
        response_data = {
            "status": "suspicious",
            "message": "Atividade incomum detectada. Por favor, complete uma verificação extra.",
            "risk_score": risk_score,
        }
        print(f"IA DETECTOU ATIVIDADE SUSPEITA: {response_data}")
    else:
        response_data = {
            "status": "ok",
            "message": "Login permitido.",
            "risk_score": risk_score,
        }
        print(f"IA APROVOU LOGIN: {response_data}")

    print("=" * 50)
    return response_data


# O módulo de IA agora funciona como blueprint integrado ao app principal
