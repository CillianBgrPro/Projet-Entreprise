const account = document.querySelector(".account");

if (account) {
    account.addEventListener("click", () => {
        window.location.href = "/compte/";
    });
}