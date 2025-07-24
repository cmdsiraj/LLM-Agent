## Setup and Installation

Follow these steps to get your AI Agent running.

### 1. Environment Setup

This section covers the general dependencies and environment preparation for your AI Agent.

#### For macOS Users:

1.  **Make `mac_setup.sh` executable:** Open your terminal, navigate to the project directory, and run:
    ```bash
    chmod +x mac_setup.sh
    ```
2.  **Run the setup script:** Execute the script to set up the required environment and install libraries:
    ```bash
    ./mac_setup.sh
    ```

#### For Windows Users:

1.  **Python Version:** Ensure you are using **Python version 3.9.6 or lower**.
2.  Create a virtual environment (if needed)
3.  **Install Dependencies:** Navigate to your project directory in the command prompt and install the necessary libraries:
    Then, install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Prepare Your Large Language Model (LLM)

Your agent is designed to work with various LLMs, and the provided code already includes integrations for Ollama and Google Gemini. Choose the LLM you wish to use and follow the respective setup steps:

**How LLM Classes are Structured:**
The agent's LLM integrations are modular. All LLM classes, such as `GeminiLLM`, extend a common `LLM` interface (or base class). This means you can easily add support for other LLMs by creating a new class that extends this interface and implements the necessary methods for interacting with that LLM. The `MyAgent.LLM` directory contains the `GeminiLLM` class, and you can add an `OllamaLLM` class (or other LLMs) there.

#### a. Option A: Using Ollama (for local models like Llama3)

If you wish to use local models like Llama3 via Ollama, follow these steps:

1.  **Download Ollama:** Visit [https://ollama.com/download](https://ollama.com/download) and download the appropriate version for your operating system.
2.  **Start the Llama3 Model:** Once Ollama is installed and running, open your terminal or command prompt and execute the following command to download and run the Llama3 model:
    ```bash
    ollama run llama3
    ```
    This command will download Llama3 if you don't have it, and then start serving it locally.
3.  **No API key is needed** for Ollama when running locally.

#### b. Option B: Using Google Gemini

To use Google Gemini, you need an API key from Google AI Studio:

1.  **Get your API Key:** Go to [Google AI Studio](https://aistudio.google.com/) and follow the instructions to obtain your Gemini API key.
2.  **Store your API Key:** The `GeminiLLM` class uses `dotenv` to load environment variables. Create a file named `.env` in your project root and add your API key like this:
    ```
    # .env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    Replace `"YOUR_GEMINI_API_KEY"` with the actual key you obtained.
    **For best results, use gemini-2.5-pro model (GeminiLLM(model_name="gemini-2.5-pro))**

#### c. Select your LLM in `agent_test.py`

In your `agent_test.py` file, you will instantiate the desired LLM class.

* **To use Google Gemini (as currently configured):**
    ```python
    from MyAgent.LLM.GeminiLLM import GeminiLLM
    # ...
    def main():
        # ...
        llm = GeminiLLM(model_name="gemini-2.0-flash-lite") # or other Gemini models like "gemini-1.5-flash"
        # ...
    ```

* **To use Ollama (assuming you have an `OllamaLLM` class):**
    ```python
    from MyAgent.LLM.OllamaLLM import OllamaLLM # You might need to create this file/class

    # ...
    def main():
        # ...
        llm = OllamaLLM(model_name="llama3") # Use the name of the model you ran via ollama
        # ...
    ```
    *(If `MyAgent/LLM/OllamaLLM.py` does not exist, you'll need to create it and implement the `LLM` interface for Ollama integration.)*

### 3. Running the Agent

Once your environment is set up and your chosen LLM is configured in `agent_test.py`, you can run the agent.

1.  **Open your terminal or command prompt.**
2.  **Navigate to your project directory.**
3.  **Run the `agent_test.py` script:**
    ```bash
    python agent_test.py
    ```
4.  The agent will start, and you can begin interacting with it by typing your natural language queries.
5.  To exit the agent, type `/exit`, `/quit`, or `/bye`.

---
