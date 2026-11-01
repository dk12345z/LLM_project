<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LLM Chat Demo</title>
    <style>
      :root {
        --bg: #f4f7fb;
        --card: #ffffff;
        --muted: #596579;
        --text: #1f2a37;
        --accent: #2563eb;
        --border: #dfe6ee;
      }

      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: var(--bg);
        color: var(--text);
      }

      .shell {
        max-width: 820px;
        margin: 48px auto;
        padding: 24px;
      }

      .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        padding: 24px;
      }

      h1 {
        margin: 0 0 20px;
        font-size: 2rem;
      }

      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
      }

      input, textarea, button {
        width: 100%;
        font: inherit;
      }

      input, textarea {
        padding: 12px 14px;
        margin-bottom: 16px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: #f9fbff;
      }

      textarea {
        height: 110px;
        resize: vertical;
      }

      button {
        border: none;
        background: var(--accent);
        color: white;
        padding: 12px 16px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
      }

      .response {
        margin-top: 20px;
        padding: 16px;
        border-radius: 10px;
        background: #eef5ff;
        border: 1px solid #d3e5ff;
        white-space: pre-wrap;
      }

      .meta {
        margin-top: 8px;
        font-size: 0.85rem;
        color: var(--muted);
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <div class="card">
        <h1>LLM Chat Demo</h1>
        <form id="chatForm">
          <label for="conversationId">Conversation ID</label>
          <input id="conversationId" name="conversation_id" value="demo-session" />

          <label for="message">Message</label>
          <textarea id="message" name="message" placeholder="Ask the assistant anything...">Hello there!</textarea>

          <button type="submit">Send</button>
        </form>

        <div id="result" class="response" hidden></div>
        <div id="meta" class="meta"></div>
      </div>
    </div>

    <script>
      const form = document.getElementById('chatForm');
      const resultBox = document.getElementById('result');
      const metaBox = document.getElementById('meta');

      form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const body = {
          conversation_id: document.getElementById('conversationId').value || 'demo-session',
          message: document.getElementById('message').value.trim(),
        };

        resultBox.hidden = false;
        resultBox.textContent = 'Sending...';
        metaBox.textContent = '';

        try {
          const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
          });

          const payload = await response.json();
          if (!response.ok) {
            throw new Error(payload.detail || 'Unknown error');
          }

          resultBox.textContent = payload.reply;
          metaBox.textContent = `Conversation: ${payload.conversation_id} | Summary: ${payload.summary || 'none'}`;
        } catch (error) {
          resultBox.textContent = `Error: ${error.message}`;
        }
      });
    </script>
  </body>
</html>
