# Brave AI Search Agent

An intelligent agent that can search the web using the Brave Search API and provide relevant information based on user queries.

## Features

- Web search using Brave Search API
- Natural language processing for better understanding of queries
- Rich console output for better readability
- Environment variable support for API keys

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your API keys:
   ```
   BRAVE_API_KEY=your_brave_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the agent:
```bash
python brave_agent.py
```

## Requirements

- Python 3.8+
- Brave Search API key
- OpenAI API key (for enhanced query processing)