const emailInput = document.getElementById("user-email");
const usernameInput = document.getElementById("id_username");
const sendCodeBtn = document.getElementById("send-code-btn");
const codeInput = document.querySelector('input[name="verification_code"]');
const statusEl = document.getElementById("code-status");
const ineInput = document.querySelector('input[name="ine"]');

let codeSent = false;
let codeValidated = false;

// Synchronise email text with username text
emailInput.addEventListener("input", () => {
    usernameInput.value = emailInput.value;
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('select option[value=""]').forEach(opt => {
        opt.disabled = true;
        opt.hidden = true;
    });
});

function togglePass(id) {
    const input = document.getElementById(id);
    input.type = input.type === "password" ? "text" : "password";
}

// event listener for code input to change button text
codeInput.addEventListener("input", () => {
    if (codeValidated) return;
    if (codeInput.value.length > 0) {
        sendCodeBtn.innerText = "Valider le code";
    } else if (codeSent) {
        sendCodeBtn.innerText = "Renvoyer le code";
    } else {
        sendCodeBtn.innerText = "Envoyer le code";
    }
});

// event listener for send code button
sendCodeBtn.addEventListener("click", function () {
    if (sendCodeBtn.innerText === "Valider le code") {
        const code = codeInput.value;
        fetch(`/verifier-code/?code=${encodeURIComponent(code)}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === "ok") {
                    statusEl.style.color = "#16a34a";
                    statusEl.textContent = "✓ Code validé !";
                    codeValidated = true;
                    sendCodeBtn.innerText = "Code validé";
                    sendCodeBtn.disabled = true;
                    codeInput.readOnly = true;
                } else {
                    statusEl.style.color = "#dc2626";
                    statusEl.textContent = "Erreur : " + data.message;
                }
            })
            .catch(() => {
                statusEl.style.color = "#dc2626";
                statusEl.textContent = "Erreur réseau. Réessayez.";
            });
        return;
    }

    const lastName = document.querySelector('input[name="last_name"]').value;
    const firstName = document.querySelector('input[name="first_name"]').value;
    const university = document.querySelector('select[name="university"]').value;
    const studyYear = document.querySelector('select[name="study_year"]').value;
    const ineValue = ineInput ? ineInput.value : "";

    if (!lastName || !firstName || !university || !studyYear || !ineValue || !ineInput.checkValidity() || !emailInput.value || !emailInput.checkValidity()) {
        statusEl.style.color = "#dc2626";
        statusEl.textContent = "Veuillez remplir toutes les informations (dont l'INE) avant d'envoyer le code.";
        return;
    }

    const email = emailInput.value;
    const btn = this;
    btn.innerText = "Envoi...";
    btn.disabled = true;
    statusEl.style.color = "#6b7280";
    statusEl.textContent = "Envoi en cours...";

    fetch(`/envoyer-code/?email=${encodeURIComponent(email)}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                statusEl.style.color = "#16a34a";
                statusEl.textContent = "✓ Code envoyé ! Vérifiez votre boîte mail.";
                btn.innerText = "Renvoyer le code";
                codeSent = true;
            } else {
                statusEl.style.color = "#dc2626";
                statusEl.textContent = "Erreur : " + data.message;
                btn.innerText = "Réessayer";
            }
            btn.disabled = false;
        })
        .catch(() => {
            statusEl.style.color = "#dc2626";
            statusEl.textContent = "Erreur réseau. Réessayez.";
            btn.innerText = "Réessayer";
            btn.disabled = false;
        });
});
