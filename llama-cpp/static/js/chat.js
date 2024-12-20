document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  let conversation = [];
  const appendMessage = (content, className) => {
    const message = document.createElement("div");
    message.className = `message ${className}`;
    console.log(content);
    message.textContent = content;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    return message.textContent
  };
  function truncateHistory(history, maxLength = 400) {
    // Convert the conversation history to a single string
    const historyStr = history.map((item) => item.content).join("\n");

    // Tokenize the string (simple tokenization by splitting on whitespace)
    const tokens = historyStr.split(/\s+/);

    // If the number of tokens exceeds the maxLength, truncate
    if (tokens.length > maxLength) {
      const truncatedTokens = tokens.slice(-maxLength); // Keep only the last `maxLength` tokens
      const truncatedHistoryStr = truncatedTokens.join(" ");

      // Reconstruct the history array with truncated content
      let tokenIndex = 0;
      return history
        .map((item) => {
          const contentTokens = item.content.split(/\s+/);
          const endIndex = tokenIndex + contentTokens.length;

          // Include only the relevant tokens for this message
          const relevantTokens = truncatedTokens.slice(tokenIndex, endIndex);
          tokenIndex = endIndex;

          return {
            ...item,
            content: relevantTokens.join(" "),
          };
        })
        .filter((item) => item.content.trim()); // Remove any empty entries
    }

    // If the number of tokens is within the limit, return the original history
    return history;
  }
  const sendMessage = async (messages) => {
    try {
      const response = await fetch("http://10.100.102.31:1234/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: messages,
          preMessage:
            "You are a helpful assistant. Your job is to give movie suggestions and to discuss movie topics with the user. you should always roleplay a human girl. if youre returning a list of movie suggestions. make sure to print them in a list.",
          
        }),
      });

      if (!response.body) {
        appendMessage("Error: No response body", "assistant-message");
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = ""; // Temporary buffer for concatenating chunks
      let assistantMessage = ""; // The assistant message to be displayed
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        // Decode the chunk and clean up unwanted strings and newline characters
        let chunk = decoder.decode(value, { stream: true }).replace(/\n/g, " ");

        // Remove unwanted strings like "|im_end|" or "|im_start|"
        chunk = chunk
          .replace(/\|\w+?_end\|/g, "")
          .replace(/\|\w+?_start\|/g, "");

        buffer += chunk;

        // Update the last message or create a new one if needed
        if (buffer.includes("assistant: ")) buffer = buffer.slice(11);

        if (
          !chatBox.lastChild ||
          !chatBox.lastChild.classList.contains("assistant-message")
        ) {
          assistantMessage = appendMessage(buffer, "assistant-message");
        } else {
          chatBox.lastChild.textContent = buffer; // Update the last message content
          assistantMessage = buffer;
        }
      }
      return assistantMessage;
    } catch (error) {
      appendMessage(`Error: ${error.message}`, "assistant-message");
    }
  };

  sendButton.addEventListener("click", async () => {
    const message = userInput.value.trim();
    if (message) {
      appendMessage(message, "user-message");
      conversation.push(
        {
          role: "user",
          content: message,
        },
      );
      conversation = truncateHistory(conversation);
      let result = await sendMessage(conversation);
      conversation.push({
        role: "assistant",
        content: result,
      });
      userInput.value = "";
    }
  });

  userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
});
