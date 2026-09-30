 async function sendMessage() {
        const inputField = document.getElementById("user-input");

        const question = inputField.value.trim();

        if (!question) return;

        appendMessage(question, "user-message");

        inputField.value = "";

        const loadingId = appendMessage("Pensando...", "bot-message loading");

        try {
          const response = await fetch("/rag/invoke", {
            method: "POST",

            headers: {
              "Content-Type": "application/json",
            },

            body: JSON.stringify({
              input: question,
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }

          const data = await response.json();

      

          document.getElementById(loadingId).remove();

    

          appendMessage(data.output, "bot-message");
        } catch (error) {
          console.error("Erro na requisição:", error);

          document.getElementById(loadingId)?.remove();

          appendMessage("Erro ao obter resposta do servidor.", "bot-message");
        }
      }

      function appendMessage(text, className) {
        const messagesContainer = document.getElementById("chat-messages");

        const messageDiv = document.createElement("div");

        const messageId = "msg-" + Date.now();

        messageDiv.id = messageId;

        messageDiv.className = `message ${className}`;

        messageDiv.innerText = text;

        messagesContainer.appendChild(messageDiv);

        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        return messageId;
      }

      function handleKeyPress(event) {
        if (event.key === "Enter") {
          sendMessage();
        }
      }