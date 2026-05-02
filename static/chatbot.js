function toggleChat() {
    const body = document.getElementById("chat-body");
    body.style.display = body.style.display === "none" ? "flex" : "none";
}

function sendMessage() {
    const input = document.getElementById("chat-input");
    const msg = input.value.trim();

    if (!msg) return;

    addMessage("You", msg);
    input.value = "";

    // 🔥 Call AI backend
    handleBotResponse(msg);
}

function addMessage(sender, text) {
    const chat = document.getElementById("chat-messages");

    const div = document.createElement("div");
    div.innerHTML = `<b>${sender}:</b> ${text}`;
    div.style.marginBottom = "8px";

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}


// 🔥 AI + Intent Logic
function handleBotResponse(msg) {

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {

        // Show AI response
        addMessage("Bot", data.reply);

        // 🔥 HANDLE INTENT
        if (data.intent === "FIND_HOSPITAL") {
            addMessage("Bot", "📍 Finding nearest hospitals...");
            findHospital();
        }

        else if (data.intent === "EMERGENCY") {
            addMessage("Bot", "🚨 Emergency detected! Finding nearest hospital...");
            findHospital();
        }

    })
    .catch(err => {
        console.error("Chat error:", err);
        addMessage("Bot", "⚠️ Unable to connect to AI right now.");
    });
}