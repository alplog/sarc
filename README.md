# SARC: Straid Agent Routing and Coordination

**SARC** is an open protocol and lightweight framework for routing messages between independent AI agents.

Instead of tightly coupled tools, SARC allows agents built with different libraries — like HuggingFace, LangChain, or OpenAI — to speak the same language via a shared communication format and a simple routing mechanism.

This project is early-stage but growing fast. It's designed with modularity in mind: agents don’t need to know anything about each other — just how to speak SARC.

## ✨ Why SARC?

Building agent-based systems usually means either:

- Reinventing orchestration from scratch
- Locking into a monolithic framework

SARC aims to be neither. It provides a middle layer — minimal, transparent, hackable — that lets agents run in different runtimes, machines, or clouds while still coordinating intelligently.

## 🧩 Core Concepts

- **Message-based architecture**  
  Agents talk by sending structured messages (requests, responses, tasks).

- **Transport-agnostic**  
  Use HTTP, WebSockets, or queues — SARC doesn't care.

- **Adapters for any stack**  
  LangChain, HuggingFace, OpenAI — just plug and route.

- **Stateless or stateful**  
  Agents can hold memory or be ephemeral.

- **Intent-based routing (SAO model)**  
  Every message carries a `subject`, `action`, and `object`.

## 📦 Project Structure
sarc/
├── core/ # router, dispatcher, coordinator
├── protocol/ # message schemas and routing logic
├── agents/ # sample agents (EchoAgent, etc.)
├── adapters/ # integration layers for frameworks
├── utils/ # helper functions, logging, config
main.py # demo runner


## 🔧 Getting Started
```bash
git clone https://github.com/yourname/sarc.git
cd sarc
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
