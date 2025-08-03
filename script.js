

// BlackCell Chatbot JS - Improved UI/UX & Features
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const modelSelect = document.getElementById("model-select");
const webSearchCheckbox = document.getElementById("web-search");
const clearBtn = document.getElementById("clear-btn");
const exportBtn = document.getElementById("export-btn");
const sendBtn = document.getElementById("sendBtn");
const clipBtn = document.getElementById("clipBtn");

let chatHistory = [];

function createBubble(sender, text, idx) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender === "You" ? "user-bubble" : "ai-bubble"}`;
  bubble.innerHTML = `
    <div class="bubble-content">
      <span class="bubble-sender">${sender}:</span>
      <span class="bubble-text" id="bubble-text-${idx}"></span>
    </div>
    <div class="bubble-actions">
      <button onclick="copyMessage(${idx})">Copy</button>
    </div>
  `;
  return bubble;
}

function appendMessage(sender, text) {
  const idx = chatHistory.length;
  const bubble = createBubble(sender, text, idx);
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
  chatHistory.push({ sender, text });
  // Animate text for AI
  if (sender === "BlackCell AI") animateText(idx, text);
  else document.getElementById(`bubble-text-${idx}`).textContent = text;
}

function animateText(idx, text) {
  let i = 0;
  const el = document.getElementById(`bubble-text-${idx}`);
  function type() {
    if (el) el.textContent = text.slice(0, i);
    if (i < text.length) {
      i++;
      setTimeout(type, 12);
    }
  }
  type();
}

function showTyping() {
  const typing = document.createElement("div");
  typing.id = "typing-msg";
  typing.className = "ai-bubble bubble typing";
  typing.innerHTML = `<em>BlackCell AI is typing<span class="dot">...</span></em>`;
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing-msg");
  if (typing) typing.remove();
}

function copyMessage(idx) {
  navigator.clipboard.writeText(chatHistory[idx].text);
}

function exportChat() {
  const text = chatHistory.map(m => `${m.sender}: ${m.text}`).join("\n");
  const blob = new Blob([text], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "chat.txt";
  a.click();
}

function clearChat() {
  chatBox.innerHTML = "";
  chatHistory = [];
  fetch("/clear", { method: "POST" });
}

function quickPrompt(prompt) {
  userInput.value = prompt;
  userInput.focus();
}

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage("You", message);
  userInput.value = "";
  showTyping();
  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: message,
      model: modelSelect ? modelSelect.value : "LLaMA3",
      web_search: webSearchCheckbox ? webSearchCheckbox.checked : false
    })
  })
    .then(res => res.json())
    .then(data => {
      removeTyping();
      if (data.reply) {
        appendMessage("BlackCell AI", data.reply);
      } else {
        appendMessage("BlackCell AI", "Error: " + (data.error || "Unknown error"));
      }
    })
    .catch(err => {
      removeTyping();
      appendMessage("BlackCell AI", "Network error: " + err.message);
    });
}

userInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
if (sendBtn) sendBtn.addEventListener("click", sendMessage);
if (clearBtn) clearBtn.addEventListener("click", clearChat);
if (exportBtn) exportBtn.addEventListener("click", exportChat);
if (clipBtn) clipBtn.addEventListener("click", () => alert("File upload coming soon!"));
