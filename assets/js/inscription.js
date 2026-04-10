/**
 * Handles the inscription process for a website.
 *
 * This script includes functionality for:
 * - Synchronizing the email input with the username input.
 * - Handling the toggle password visibility feature.
 * - Managing the state of code validation and sending.
 */

const emailInput = document.getElementById("user-email"); // Input field for user's email
const usernameInput = document.getElementById("id_username"); // Input field for user's username, synchronized with email
const sendCodeBtn = document.getElementById("send-code-btn"); // Button to send verification code
const codeInput = document.querySelector('input[name="verification_code"]'); // Input field for the verification code
const statusEl = document.getElementById("code-status"); // Element to display status messages
const ineInput = document.querySelector('input[name="ine"]'); // Input field for INE number (optional)

let codeSent = false; // Flag to track if a code has been sent
let codeValidated = false; // Flag to track if the verification code has been validated

// Event listener to synchronize email input with username input
emailInput.addEventListener("input", () => {
    usernameInput.value = emailInput.value;
});

document.addEventListener("DOMContentLoaded", function () {
    /**
     * Disables and hides empty options in select elements.
     */
    document.querySelectorAll('select option[value=""]').forEach(opt => {
        opt.disabled = true;
        opt.hidden = true;
    });
});

/**
 * Toggles the visibility of a password input field.
 *
 * @param {string} id - The ID of the input field to toggle.
 * @param {HTMLElement} btn - The button element associated with the input field.
 */
function togglePass(id, btn) {
    const input = document.getElementById(id); // Password input field
    const icon = btn.querySelector('span'); // Icon inside the button

    if (input.type === 'password') {
        input.type = 'text'; // Change input type to text to show password
        icon.textContent = 'visibility'; // Update button icon to indicate visibility
    } else {
        input.type = 'password'; // Change input type back to password to hide password
        icon.textContent = 'visibility_off'; // Update button icon to indicate hidden password
    }
}

// Event listener for code input to change button text based on user interaction
codeInput.addEventListener("input", () => {
    if (codeValidated) return; // Skip if the code has already been validated

    if (codeInput.value.length > 0) {
        sendCodeBtn.innerText = "Valider le code"; // Change button text to 'Validate Code'
    } else if (codeSent) {
        sendCodeBtn.innerText = "Renvoyer le code"; // Change button text to 'Resend Code'
    } else {
        sendCodeBtn.innerText = "Envoyer le code"; // Change button text to 'Send Code'
    }
});

/**
 * Event listener for the "sendCodeBtn" button click.
 * Handles the process of sending a verification code based on the user's input.
 */
sendCodeBtn.addEventListener("click", function () {
    // Check if the current inner text is "Valider le code"
    if (sendCodeBtn.innerText === "Valider le code") {
        // Retrieve the code from the input field
        const code = codeInput.value;
        
        // Send a fetch request to verify the code
        fetch(`/verifier-code/?code=${encodeURIComponent(code)}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === "ok") {
                    // Update UI if the code is valid
                    statusEl.style.color = "#16a34a";
                    statusEl.textContent = "✓ Code validé !";
                    codeValidated = true;
                    sendCodeBtn.innerText = "Code validé";
                    sendCodeBtn.disabled = true;
                    codeInput.readOnly = true;
                } else {
                    // Update UI if the code is invalid
                    statusEl.style.color = "#dc2626";
                    statusEl.textContent = "Erreur : " + data.message;
                }
            })
            .catch(() => {
                // Update UI if there's a network error
                statusEl.style.color = "#dc2626";
                statusEl.textContent = "Erreur réseau. Réessayez.";
            });
        return;
    }

    // Retrieve user input values
    const lastName = document.querySelector('input[name="last_name"]').value;
    const firstName = document.querySelector('input[name="first_name"]').value;
    const university = document.querySelector('select[name="university"]').value;
    const studyYear = document.querySelector('select[name="study_year"]').value;
    const ineValue = ineInput ? ineInput.value : "";
    
    // Validate user input
    if (!lastName || !firstName || !university || !studyYear || !ineValue || !ineInput.checkValidity() || !emailInput.value || !emailInput.checkValidity()) {
        statusEl.style.color = "#dc2626";
        statusEl.textContent = "Veuillez remplir toutes les informations (dont l'INE) avant d'envoyer le code.";
        return;
    }

    // Retrieve email value
    const email = emailInput.value;
    
    // Update button state during the sending process
    const btn = this;
    btn.innerText = "Envoi...";
    btn.disabled = true;
    statusEl.style.color = "#6b7280";
    statusEl.textContent = "Envoi en cours...";

    // Send a fetch request to send the verification code via email
    fetch(`/envoyer-code/?email=${encodeURIComponent(email)}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                // Update UI if the code is sent successfully
                statusEl.style.color = "#16a34a";
                statusEl.textContent = "✓ Code envoyé ! Vérifiez votre boîte mail.";
                btn.innerText = "Renvoyer le code";
                codeSent = true;
            } else {
                // Update UI if there's an error sending the code
                statusEl.style.color = "#dc2626";
                statusEl.textContent = "Erreur : " + data.message;
                btn.innerText = "Réessayer";
            }
            btn.disabled = false;
        })
        .catch(() => {
            // Update UI if there's a network error during the sending process
            statusEl.style.color = "#dc2626";
            statusEl.textContent = "Erreur réseau. Réessayez.";
            btn.innerText = "Réessayer";
            btn.disabled = false;
        });
});
