const widgetScript = document.currentScript;
const API_ENDPOINT =
  widgetScript?.dataset.ronbotEndpoint ||
  "https://9jf25kxi10.execute-api.eu-west-2.amazonaws.com/ask";
const WIDGET_ASSET_DIRECTORY = widgetScript?.src
  ? new URL(".", widgetScript.src).href
  : "assets/";
const RONBOT_IMAGE =
  widgetScript?.dataset.ronbotImage ||
  new URL("ronbot-production.png", WIDGET_ASSET_DIRECTORY).href;

function loadRonBotStyles() {
  if (document.querySelector("link[data-ronbot-styles]")) {
    return;
  }

  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = new URL("ronbot.css", WIDGET_ASSET_DIRECTORY).href;
  stylesheet.dataset.ronbotStyles = "true";
  document.head.appendChild(stylesheet);
}

function initialiseRonBot() {
  if (document.getElementById("ronbot-widget")) {
    return;
  }

  loadRonBotStyles();

  document.body.insertAdjacentHTML(
    "beforeend",
    `
      <section id="ronbot-widget" class="ronbot-widget">
        <div
          id="ronbot-chat-panel"
          class="ronbot-chat-panel"
          role="dialog"
          aria-labelledby="ronbot-title"
          aria-hidden="true"
        >
          <div class="ronbot-chat-header">
            <div>
              <strong id="ronbot-title">RonBot</strong>
              <span>Portfolio assistant</span>
            </div>
            <button
              id="ronbot-close"
              class="ronbot-close"
              type="button"
              aria-label="Close RonBot chat"
            >×</button>
          </div>
          <div id="ronbot-messages" class="ronbot-chat-messages" aria-live="polite">
            <div class="ronbot-message ronbot-message-bot">
              Hi, I’m RonBot. Ask me about Ron’s experience, skills, education,
              certifications or projects.
            </div>
          </div>
          <form id="ronbot-form" class="ronbot-chat-form">
            <label class="ronbot-visually-hidden" for="ronbot-input">Ask RonBot a question</label>
            <input
              id="ronbot-input"
              type="text"
              placeholder="Ask RonBot something..."
              autocomplete="off"
            >
            <button type="submit">Send</button>
          </form>
        </div>
        <button
          id="ronbot-launcher"
          class="ronbot-launcher"
          type="button"
          aria-label="Open RonBot"
          aria-expanded="false"
        >
          <img src="${RONBOT_IMAGE}" alt="RonBot">
        </button>
      </section>
    `,
  );

  const launcher = document.getElementById("ronbot-launcher");
  const chatPanel = document.getElementById("ronbot-chat-panel");
  const closeButton = document.getElementById("ronbot-close");
  const form = document.getElementById("ronbot-form");
  const input = document.getElementById("ronbot-input");
  const messages = document.getElementById("ronbot-messages");
  let greetingTimer;

  function playGreeting() {
    window.clearTimeout(greetingTimer);
    launcher.classList.remove("ronbot-greeting");
    void launcher.offsetWidth;
    launcher.classList.add("ronbot-greeting");
    greetingTimer = window.setTimeout(() => {
      launcher.classList.remove("ronbot-greeting");
    }, 900);
  }

  function openChat() {
    chatPanel.classList.add("ronbot-chat-open");
    launcher.classList.add("ronbot-active");
    chatPanel.setAttribute("aria-hidden", "false");
    launcher.setAttribute("aria-expanded", "true");
    playGreeting();
    input.focus();
  }

  function closeChat() {
    chatPanel.classList.remove("ronbot-chat-open");
    launcher.classList.remove("ronbot-active", "ronbot-greeting");
    chatPanel.setAttribute("aria-hidden", "true");
    launcher.setAttribute("aria-expanded", "false");
    launcher.focus();
  }

  function addBotMessage(text) {
    const messageBubble = document.createElement("div");
    messageBubble.classList.add("ronbot-message", "ronbot-message-bot");
    messageBubble.textContent = text;
    messages.appendChild(messageBubble);
    messages.scrollTop = messages.scrollHeight;
  }

  function setThinking(isThinking) {
    launcher.classList.toggle("ronbot-thinking", isThinking);
    if (isThinking) {
      launcher.classList.remove("ronbot-greeting");
    }
  }

  launcher.addEventListener("click", () => {
    if (chatPanel.classList.contains("ronbot-chat-open")) {
      closeChat();
    } else {
      openChat();
    }
  });

  closeButton.addEventListener("click", closeChat);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && chatPanel.classList.contains("ronbot-chat-open")) {
      closeChat();
    }
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) {
      return;
    }

    const messageBubble = document.createElement("div");
    messageBubble.classList.add("ronbot-message", "ronbot-message-user");
    messageBubble.textContent = message;
    messages.appendChild(messageBubble);
    input.value = "";
    messages.scrollTop = messages.scrollHeight;
    setThinking(true);

    const thinkingMessage = document.createElement("div");
    thinkingMessage.classList.add(
      "ronbot-message",
      "ronbot-message-bot",
      "ronbot-thinking-message",
    );
    thinkingMessage.innerHTML = `
      <span>RonBot is thinking</span>
      <span class="ronbot-dots" aria-hidden="true"><span>.</span><span>.</span><span>.</span></span>
    `;
    messages.appendChild(thinkingMessage);
    messages.scrollTop = messages.scrollHeight;

    fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message }),
    })
      .then((response) => {
        if (!response.ok) {
          const error = new Error("RonBot API request failed.");
          error.status = response.status;
          throw error;
        }
        return response.json();
      })
      .then((data) => {
        thinkingMessage.remove();
        addBotMessage(data.answer);
        setThinking(false);
      })
      .catch((error) => {
        thinkingMessage.remove();
        addBotMessage(
          error.status === 429
            ? "RonBot is receiving a lot of requests right now. Please wait a moment and try again."
            : "RonBot is having trouble connecting right now. Please try again shortly.",
        );
        setThinking(false);
        console.error(error);
      });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initialiseRonBot);
} else {
  initialiseRonBot();
}
