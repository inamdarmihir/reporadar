# 🚀 GitHub Trending Agent with Agno

A production-ready AI agent for discovering GitHub trending repositories using natural language, powered by **Agno Framework** and **Claude Sonnet 4.5**.

## ✨ Features

- **🔍 Natural Language Search**: Ask questions in plain English about repositories
- **📈 Trending Discovery**: Get daily, weekly, or monthly trending repos
- **🔥 Hot New Projects**: Find recently created popular repositories  
- **🧠 Long-term Memory**: Agent remembers your preferences and search history
- **💻 Language Filtering**: Filter by any programming language
- **🎯 Personalized Recommendations**: Get suggestions based on your interests
- **🚀 Production Ready**: FastAPI server with REST API endpoints

## 🏗️ Architecture

Built with:
- **Agno Framework**: Modern Python framework for AI agents
- **Claude Sonnet 4.5**: Advanced reasoning and natural language understanding
- **SQLite Storage**: Persistent conversation memory
- **FastAPI**: High-performance REST API
- **GitHub Data**: Real-time scraping + REST API integration

## 📦 Installation

### Prerequisites

- Python 3.10+
- API Keys: Anthropic (required), GitHub Token (optional but recommended)

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/inamdarmihir/reporadar.git
cd reporadar
```

2. **Install dependencies**:
```bash
pip install -e .
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required in `.env`:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional but recommended
```

4. **Run the agent**:
```bash
# Interactive CLI
python app.py

# Or start the API server
python api.py
```

## 🎮 Usage

### Using Python SDK

```python
from app import agent

# Simple query
response = agent.run("What are the trending Python repositories today?")
print(response.content)

# With session memory
response = agent.run(
    "Remember that I prefer Rust and Go",
    session_id="user-123"
)

# Get personalized recommendations
response = agent.run(
    "What's trending that I might like?",
    session_id="user-123"
)
```

### Using REST API

Start the server:
```bash
python api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

Make requests:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find trending Rust projects",
    "session_id": "user-123"
  }'
```

### Running Examples

```bash
# Basic usage examples
python examples/basic_usage.py

# Memory and personalization examples
python examples/with_memory.py
```

## 🛠️ Available Tools

The agent has access to these tools:

### 1. `get_trending_repos`
Fetches trending repositories from GitHub.

**Parameters:**
- `language` (str): Programming language filter (optional)
- `time_period` (str): 'daily', 'weekly', or 'monthly'

### 2. `search_repos`
Searches GitHub repositories using natural language.

**Parameters:**
- `query` (str): Natural language search query
- `max_results` (int): Number of results (1-10)

### 3. `get_hot_repos`
Finds recently created popular repositories.

**Parameters:**
- `language` (str): Programming language filter (optional)
- `days` (int): Look back N days (1-30)

## 📊 Project Structure

```
.
├── app.py                  # Main agent implementation
├── api.py                  # FastAPI server
├── pyproject.toml          # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
└── examples/
    ├── basic_usage.py      # Basic usage examples
    └── with_memory.py      # Memory & personalization examples
```

## 🧠 Memory System

The agent uses Agno's built-in SQLite storage for persistent memory:

### Conversation History
- Maintains context across multiple interactions
- Remembers up to 5 previous exchanges per session
- Session-based isolation for multi-user scenarios

### User Preferences
Automatically stores and recalls:
- Preferred programming languages
- Topics of interest
- Search patterns
- Feedback and interactions

## 💬 Example Conversations

### Basic Usage
```
User: What are the trending Python repositories today?
Agent: [Shows top 10 trending Python repos with details]

User: Find machine learning frameworks
Agent: [Searches and displays relevant ML repositories]
```

### With Memory
```
User: Remember that I prefer Go and Rust for systems programming
Agent: I'll remember that you prefer Go and Rust for systems programming!

User: What's trending this week that I might like?
Agent: [Uses stored preferences to filter and recommend]

User: What do you remember about my preferences?
Agent: [Retrieves and displays stored information]
```

### Advanced Queries
```
User: I'm learning web development, what should I check out?
Agent: [Provides curated recommendations]

User: Show me the hottest repos from the last 3 days in TypeScript
Agent: [Fetches and displays recent popular TypeScript projects]
```

## 🚀 Deployment

### Local Development
```bash
# Run agent directly
python app.py

# Or run API server with auto-reload
python api.py
```

### Production Deployment

The agent can be deployed to any platform that supports Python:

**Docker**:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "api.py"]
```

**Cloud Platforms**:
- AWS Lambda / ECS
- Google Cloud Run
- Azure Container Apps
- Railway / Render / Fly.io

## 🔧 Configuration

### Agent Settings

Edit `app.py` to customize:
- Model selection (Claude, GPT, Gemini, etc.)
- Temperature and creativity
- Number of history messages
- Tool configurations
- System instructions

### API Settings

Edit `api.py` to customize:
- Port and host
- CORS settings
- Rate limiting
- Authentication

## 🐛 Troubleshooting

### Issue: "Module 'agno' not found"
**Solution**: Install dependencies: `pip install -e .`

### Issue: "API key not found"
**Solution**: Ensure `.env` file exists with valid `ANTHROPIC_API_KEY`

### Issue: "Rate limit exceeded"
**Solution**: Add GitHub token to `.env` for higher limits (60 → 5000 req/hour)

### Issue: "No trending repositories found"
**Solution**: GitHub's HTML structure may have changed. Check scraper in `app.py`

## 📚 Learn More

- **Agno Framework**: https://agno.com
- **Agno Docs**: https://docs.agno.com
- **Claude API**: https://docs.anthropic.com/
- **GitHub API**: https://docs.github.com/en/rest

## 🎯 Key Agno Concepts

### Agent
The core `Agent` class handles:
- Model integration (Claude, GPT, Gemini, etc.)
- Tool management and execution
- Memory and state persistence
- Conversation flow

### Tools
Functions decorated with `@tool` that the agent can call:
- Automatically parsed and validated
- Type-safe with Pydantic
- Easy to add custom tools

### Storage
SQLite-based persistent storage:
- Session management
- Conversation history
- User preferences
- Cross-session memory

### Models
Model-agnostic design:
- Easy to switch between providers
- Consistent API across models
- Support for streaming responses

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more GitHub data sources (GitLab, Bitbucket)
- Implement code analysis features
- Add visualization tools
- Build custom UI
- Extend memory capabilities
- Add more tools

## 📄 License

MIT License - Use freely in your projects!

## 🙏 Acknowledgments

- **Anthropic** for Claude
- **Agno team** for the amazing framework
- **GitHub** for trending data
- **Open source community**

---

**Built with ❤️ using Agno Framework**

**Migration from LangGraph to Agno** - v2.0.0

For issues or questions:
- [GitHub Issues](https://github.com/inamdarmihir/reporadar/issues)
- [Agno Discord](https://discord.gg/agno)
