# React Agent Calculator

A simple ReAct agent using LangChain and Ollama.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running

## Setup

1. **Install Ollama**:
   Visit [https://ollama.ai](https://ollama.ai) and follow the installation instructions for your platform.

2. **Pull the Ollama model**:
   ```bash
   ollama pull qwen2.5:7b
   ```

3. **Create virtual environment and install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

1. **Start Ollama** (in a separate terminal):
   ```bash
   ollama serve
   ```

2. **Run the agent**:
   ```bash
   source venv/bin/activate
   python agent.py
   ```

3. **Enter your queries**:
   ```
   📝 Enter your query: What is 25 times 8?
   ```

4. **Exit**: Type `exit` or `quit`

