document.getElementById("send").addEventListener("click", async function () {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    let chatContainer = document.getElementById("chat-container");

    // Tambahkan pesan pengguna
    let userMessage = `<div class="bubble user">${userInput}</div>`;
    chatContainer.innerHTML += userMessage;

    document.getElementById("user-input").value = "";

    try {
        let response = await fetch("https://web-production-5bbc.up.railway.app/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();

        let botMessage = `<div class="bubble bot">${data.response}</div>`;
        chatContainer.innerHTML += botMessage;
    } catch (error) {
        console.error("Error:", error);
        let errorMessage = `<div class="bubble bot">⚠️ Error, coba lagi.</div>`;
        chatContainer.innerHTML += errorMessage;
    }
});
