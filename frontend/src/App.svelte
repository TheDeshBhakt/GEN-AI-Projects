<script>
  import { onMount } from 'svelte';

  let messages = [];
  let userInput = '';
  let isLoading = false;
  const backendUrl = 'http://localhost:8000/api/chat'; // The FastAPI backend URL

  // Add a welcome message when the component mounts
  onMount(() => {
    messages = [
      {
        id: Date.now(),
        text: 'Namaste! Welcome to the Varanasi AI Guide. How can I help you today?',
        sender: 'ai',
      },
    ];
  });

  async function handleSubmit() {
    if (!userInput.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: userInput,
      sender: 'user',
    };

    messages = [...messages, userMessage];
    isLoading = true;
    userInput = ''; // Clear the input

    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const aiMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'ai',
      };
      messages = [...messages, aiMessage];

    } catch (error) {
      console.error('Error fetching from backend:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I am having trouble connecting to my knowledge base. Please try again later.',
        sender: 'ai',
        isError: true,
      };
      messages = [...messages, errorMessage];
    } finally {
      isLoading = false;
    }
  }
</script>

<main>
  <div class="header">
    <h1>Varanasi AI Guide</h1>
    <p>Your digital companion for exploring the city of light</p>
  </div>

  <div class="chat-window">
    {#each messages as message (message.id)}
      <div class="message {message.sender === 'user' ? 'user-message' : 'ai-message'}">
        <p>{message.text}</p>
      </div>
    {/each}
    {#if isLoading}
      <div class="message ai-message loading">
        <p>Thinking...</p>
      </div>
    {/if}
  </div>

  <form on:submit|preventDefault={handleSubmit}>
    <input
      type="text"
      bind:value={userInput}
      placeholder="Ask about places, stories, or development..."
      disabled={isLoading}
    />
    <button type="submit" disabled={isLoading}>Send</button>
  </form>
</main>

<style>
  :root {
    --primary-color: #FF9933; /* Saffron */
    --secondary-color: #FFFFFF; /* White */
    --text-color: #333;
    --ai-message-bg: #f1f1f1;
    --user-message-bg: #e6f2ff;
    --border-color: #ddd;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 768px;
    margin: 0 auto;
    border: 1px solid var(--border-color);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .header {
    background-color: var(--primary-color);
    color: var(--secondary-color);
    padding: 1rem;
    text-align: center;
  }

  .header h1 {
    margin: 0;
    font-size: 1.5rem;
  }
    .header p {
    margin: 0;
    font-size: 0.9rem;
    }

  .chat-window {
    flex-grow: 1;
    padding: 1rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message {
    padding: 0.5rem 1rem;
    border-radius: 18px;
    max-width: 80%;
  }

  .ai-message {
    background-color: var(--ai-message-bg);
    align-self: flex-start;
    border-bottom-left-radius: 4px;
  }

  .user-message {
    background-color: var(--user-message-bg);
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  }

  .message p {
    margin: 0;
    white-space: pre-wrap; /* To respect newlines in the response */
  }

  .loading p {
    font-style: italic;
    color: #888;
  }

  form {
    display: flex;
    padding: 1rem;
    border-top: 1px solid var(--border-color);
  }

  input {
    flex-grow: 1;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    font-size: 1rem;
  }

  button {
    background-color: var(--primary-color);
    color: var(--secondary-color);
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 20px;
    margin-left: 0.5rem;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.2s;
  }

  button:hover {
    background-color: #e68a2e;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
</style>
