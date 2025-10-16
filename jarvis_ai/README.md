# 🤖 Jarvis — Intelligent Voice Assistant

Jarvis is a **voice-enabled AI assistant** built using **Python**, **LangChain**, and **LiveKit**, developed by **Mohd Shehzad**.  
It communicates naturally in **Hinglish** (a mix of Hindi and English), making interactions feel conversational and personalized. Its reasoning capabilities are powered by **LangChain Agent Mode**.

---

## 🚀 Project Overview

Unlike traditional chatbots, Jarvis is a **thinking assistant** capable of:

- Understanding and responding in Hinglish  
- Conversing with personality, humor, and context  
- Providing real-time information such as **date, location, and weather**  
- Leveraging LangChain Agents for decision-making and tool usage  
- Speaking naturally using **LiveKit’s voice streaming**  

This project demonstrates **integration of LLMs with real-world APIs** to create a voice-based assistant with contextual reasoning.

---

## 🧠 Technology Stack

| Component   | Purpose |
|------------|---------|
| Python     | Main programming language for development |
| LangChain  | Enables reasoning and tool integration for AI |
| LiveKit    | Powers real-time voice communication |
| AsyncIO    | Handles asynchronous API calls and tasks |
| Requests   | Fetches user’s city based on IP |
| Custom APIs| Provides weather and time information |

---

## ⚙️ Features

- 🗣️ **Voice Interaction:** Communicate with Jarvis in real-time  
- 💬 **Hinglish Conversation:** Natural Indian-style dialogue  
- 🌦️ **Dynamic Context:** Automatically fetches date, location, and weather  
- 🧩 **Reasoning Mode:** Uses LangChain Agent for decision-making  
- 🧠 **Personality:** Witty, polite, and engaging assistant responses  
- ⚡ **Asynchronous Execution:** Smooth performance using async functions  

---

## 📂 Getting the Code

Clone the repository using:

```bash
git clone https://github.com/Shehzadchouhan/ai-ml-training-diary/tree/0d6ae3aa2399763c48210eb217c132a28ff322cf/jarvis_main/jarvis_3.0

🏃 How to Run Jarvis

Create a virtual environment:

python -m venv venv


Activate the environment:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the assistant:

python agent.py console
