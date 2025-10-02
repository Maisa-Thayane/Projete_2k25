document.addEventListener("DOMContentLoaded", () => {
    // Este script não faz nenhuma validação do lado do cliente.
    // O formulário será sempre enviado ao Flask para processamento.
    // Todas as mensagens de erro serão geradas pelo servidor (Flask).
    // O parágrafo de erro no HTML será preenchido pelo Flask.
});

// Dados comportamentais em tempo real
let behavioralData = {
    mouse_movements: [],
    key_press_times: [],
    click_events: [],
    start_time: Date.now()
};

// Limites para evitar o acúmulo excessivo de dados
const MAX_MOUSE_MOVEMENTS = 500; // Limite o número de movimentos do mouse a serem armazenados
const MAX_KEY_PRESSES = 200; // Limite o número de tempos de pressionamento de tecla a serem armazenados
const MAX_CLICK_EVENTS = 100; // Limite o número de eventos de clique a serem armazenados

// Capturar movimentos do mouse
document.addEventListener('mousemove', function (e) {
    behavioralData.mouse_movements.push({
        x: e.clientX,
        y: e.clientY,
        time: Date.now() - behavioralData.start_time
    });

    if (mouseMovements.length < MAX_MOUSE_MOVEMENTS) {
        mouseMovements.push({ x: e.clientX, y: e.clientY, time: Date.now() });
    }
});

// Capturar pressionamentos de tecla
document.addEventListener('keydown', function (e) {
    behavioralData.key_press_times.push({
        key: e.key,
        time: Date.now() - behavioralData.start_time
    });

    if (keyPressTimes.length < MAX_KEY_PRESSES) {
        keyPressTimes.push({ key: e.key, time: Date.now() });
    }
});

// Capturar cliques
document.addEventListener('click', function (e) {
    behavioralData.click_events.push({
        x: e.clientX,
        y: e.clientY,
        time: Date.now() - behavioralData.start_time
    });

    if (clickEvents.length < MAX_CLICK_EVENTS) {
        clickEvents.push({ x: e.clientX, y: e.clientY, time: Date.now(), target: e.target.tagName });
    }
});

// Interceptar o envio do formulário para incluir dados comportamentais
document.querySelector('.formulario').addEventListener('submit', function (e) {
    // Adicionar dados comportamentais ao formulário
    const behavioralInput = document.createElement('input');
    behavioralInput.type = 'hidden';
    behavioralInput.name = 'behavioral_data';
    behavioralInput.value = JSON.stringify(behavioralData);
    this.appendChild(behavioralInput);

    console.log('Dados comportamentais capturados:', behavioralData);
});