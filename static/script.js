document.getElementById("send").addEventListener("click", async function () {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return; // Cegah input kosong

    let chatContainer = document.getElementById("chat-container");

    // Tambahkan pesan pengguna ke UI
    let userMessage = `<div class="bubble user">${userInput}</div>`;
    chatContainer.innerHTML += userMessage;

    document.getElementById("user-input").value = ""; // Kosongkan input

    try {
        let response = await fetch("https://web-production-5bbc.up.railway.app/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();

        // Tambahkan pesan bot ke UI
        let botMessage = `<div class="bubble bot">${data.response}</div>`;
        chatContainer.innerHTML += botMessage;
    } catch (error) {
        console.error("Error:", error);
        let errorMessage = `<div class="bubble bot">⚠️ Error, coba lagi.</div>`;
        chatContainer.innerHTML += errorMessage;
    }
});
