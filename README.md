# My Local Chatbot

A local chatbot built using **Streamlit**, **LangChain**, and **Ollama**.  
Supports multi-turn conversations and maintains chat history in SQLite.

## Features
- Uses a local LLM via Ollama (e.g., llama3.2:3b)
- Structured prompts with LangChain
- Stores chat history per user in SQLite
- Real-time streaming responses with Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Janakivallabh/my_chatbot.git
cd my_chatbot
```

2. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
- Fill in your own API key and project details.

5. Run the chatbot:
```bash
streamlit run app.py
```

## Usage
- Enter a **user ID** to start a conversation.
- Type messages in the chat input box.
- Click **Start New Conversation** to clear history.

## Notes
- Ensure **Ollama LLM** is running locally (`ollama run llama3.2:3b`).
- Chat history is stored locally in `chat_history.db`.
