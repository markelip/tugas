document.getElementById("send").addEventListener("click", async function () {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    let chatContainer = document.getElementById("chat-container");
    chatContainer.innerHTML += `<div class="bubble user">${userInput}</div>`;
    document.getElementById("user-input").value = "";

    try {
        let response = await fetch("https://web-production-5bbc.up.railway.app/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();
        chatContainer.innerHTML += `<div class="bubble bot">${data.response}</div>`;
    } catch (error) {
        console.error("Error:", error);
        chatContainer.innerHTML += `<div class="bubble bot">⚠️ Error, coba lagi.</div>`;
    }
});
