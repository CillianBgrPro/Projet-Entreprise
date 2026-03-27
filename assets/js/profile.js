const account = document.querySelector(".account");

account.addEventListener("click", () => {
    window.location.href = "{% url 'compte' %}";
});