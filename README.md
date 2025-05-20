# 🧠 DebateMyTicket

A multi-agent legal reasoning assistant for ticket disputes. Upload your ticket image and let AI agents debate whether you should pay or challenge it.

## Features

- 📸 Image upload and OCR processing
- 🔍 Legal and social context gathering
- 🤖 AI-powered debate between pro-payment and anti-payment agents
- ✅ Ticket validation and legal flaw detection
- 📊 Real-time debate visualization
- 💾 Debate history saving

## Tech Stack

- Python 3.8+
- Streamlit - Frontend
- LangGraph - Multi-agent state management
- LiteLLM - GPT-4 interface
- Tesseract - OCR processing
- BeautifulSoup4 - Web scraping
- OpenAI GPT-4 - Language model
- uv - Python packaging & environment management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DebateMyTicket.git
cd DebateMyTicket
```

2. Install uv if you haven't already:
```bash
pip install uv
```

3. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies using uv:
```bash
uv sync
```

5. Set up your OpenAI API key:
   - Create an `api.cfg` file in the project root
   - Add your API key:
```ini
[openai]
api_key = your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a ticket image and optionally provide additional context

4. Click "Analyze Ticket" to start the debate

## Project Structure

```
DebateMyTicket/
│
├── app.py                   # Streamlit frontend
├── debate_my_ticket/        # Core package
│   ├── agents/
│   │   ├── pro_payment.py   # Pro-payment agent logic
│   │   └── anti_payment.py  # Anti-payment agent logic
│   │
│   ├── backend/
│   │   ├── ocr_processor.py # OCR and image parsing
│   │   ├── info_scraper.py  # Legal info, tweets, Reddit scraping
│   │   └── ticket_validator.py  # Ticket validation
│   │
│   ├── utils/
│   │   ├── prompts.py       # Prompt templates
│   │   └── helpers.py       # Utility functions
│   │
│   └── langgraph_runner.py  # LangGraph graph construction and execution
│
├── api.cfg                 # API configuration
├── pyproject.toml          # Project dependencies
└── README.md               # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4
- Streamlit team for the amazing frontend framework
- LangGraph team for the multi-agent framework
- uv team for the fast Python package manager
