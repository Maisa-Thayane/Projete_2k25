document.addEventListener("DOMContentLoaded", () => {
    // Seleciona todos os campos de entrada de dígito
    const inputDigits = document.querySelectorAll(".verification-input-digit");
    const confirmButton = document.getElementById("confirmButton");
    const messageDisplay = document.getElementById("messageDisplay");

    // Adiciona o evento para cada campo de entrada
    inputDigits.forEach((input, index) => {
        input.addEventListener("input", (event) => {
            // Remove qualquer caractere que não seja um dígito
            input.value = input.value.replace(/\D/g, "");

            // Se um dígito foi inserido e não é o último campo, move o foco para o próximo
            if (input.value.length === 1 && index < inputDigits.length - 1) {
                inputDigits[index + 1].focus();
            }

            // Ativa o botão de confirmação se todos os campos estiverem preenchidos
            const allFilled = Array.from(inputDigits).every(digit => digit.value.length === 1);
            confirmButton.disabled = !allFilled;
        });

        input.addEventListener("keydown", (event) => {
            // Se a tecla "Backspace" for pressionada e o campo atual está vazio, move o foco para o anterior
            if (event.key === "Backspace" && input.value === "" && index > 0) {
                inputDigits[index - 1].focus();
            }
        });
    });

    // Adiciona o evento de clique ao botão de confirmação
    confirmButton.addEventListener("click", () => {
        // Concatena todos os valores dos campos para formar o código completo
        let fullCode = "";
        inputDigits.forEach(input => {
            fullCode += input.value;
        });

        // Verifica se o código completo tem exatamente 4 dígitos
        if (fullCode.length !== 4) {
            messageDisplay.textContent = "Por favor, preencha todos os 4 dígitos.";
            return;
        }

        // Desabilita o botão para evitar cliques múltiplos
        confirmButton.disabled = true;
        
        // Envia o código digitado para o servidor para validação
        fetch("/verify-code", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code: fullCode }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageDisplay.textContent = "Código correto! Redirecionando...";
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 2000); // Redireciona após 2 segundos
            } else {
                messageDisplay.textContent = data.error;
                confirmButton.disabled = false; // Habilita o botão novamente
            }
        })
        .catch(error => {
            console.error("Erro na comunicação com o servidor:", error);
            messageDisplay.textContent = "Erro ao verificar o código. Tente novamente.";
            confirmButton.disabled = false; // Habilita o botão novamente
        });
    });
});