const launcher = document.getElementById("ronbot-launcher");
const chatPanel = document.getElementById("ronbot-chat-panel");
const closeButton = document.getElementById("ronbot-close");

function openChat() {
  chatPanel.classList.add("ronbot-chat-open");
  launcher.classList.add("ronbot-active");

  chatPanel.setAttribute("aria-hidden", "false");
  launcher.setAttribute("aria-expanded", "true");
}

function closeChat() {
  chatPanel.classList.remove("ronbot-chat-open");
  launcher.classList.remove("ronbot-active");

  chatPanel.setAttribute("aria-hidden", "true");
  launcher.setAttribute("aria-expanded", "false");
}

launcher.addEventListener("click", () => {
  const isOpen = chatPanel.classList.contains("ronbot-chat-open");

  if (isOpen) {
    closeChat();
  } else {
    openChat();
  }
});

const form = document.getElementById("ronbot-form");
const input = document.getElementById("ronbot-input");
const messages = document.getElementById("ronbot-messages");

function addBotMessage(text) {
  const messageBubble = document.createElement("div");

  messageBubble.classList.add(
    "ronbot-message",
    "ronbot-message-bot"
  );

  messageBubble.textContent = text;

  messages.appendChild(messageBubble);
  messages.scrollTop = messages.scrollHeight;

  return messageBubble;
}

function setThinking(isThinking) {
  launcher.classList.toggle("ronbot-thinking", isThinking);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const message = input.value.trim();

  if (!message) {
    return;
  }

  const messageBubble = document.createElement("div");

  messageBubble.classList.add(
    "ronbot-message",
    "ronbot-message-user"
  );

  messageBubble.textContent = message;

  messages.appendChild(messageBubble);

  input.value = "";
  messages.scrollTop = messages.scrollHeight;

  setThinking(true);

const thinkingMessage = document.createElement("div");

thinkingMessage.classList.add(
  "ronbot-message",
  "ronbot-message-bot",
  "ronbot-thinking-message"
);

thinkingMessage.innerHTML = `
  <span>RonBot is thinking</span>
  <span class="ronbot-dots" aria-hidden="true">
    <span>.</span>
    <span>.</span>
    <span>.</span>
  </span>
`;

messages.appendChild(thinkingMessage);
messages.scrollTop = messages.scrollHeight;

  setTimeout(() => {
    thinkingMessage.remove();

    addBotMessage(
      "Test response: I’ll answer this from Ron’s website knowledge base."
    );

    setThinking(false);
  }, 1800);
});

closeButton.addEventListener("click", closeChat);