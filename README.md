# 🚀 GitHub Trending Agent with Langmem

A production-ready LangGraph agent for discovering GitHub trending repositories using natural language, powered by Claude Sonnet 4.5 and Langmem for long-term memory.

## ✨ Features

- **🔍 Natural Language Search**: Ask questions in plain English about repositories
- **📈 Trending Discovery**: Get daily, weekly, or monthly trending repos
- **🔥 Hot New Projects**: Find recently created popular repositories  
- **🧠 Long-term Memory**: Agent remembers your preferences and search history
- **💻 Language Filtering**: Filter by any programming language
- **🎯 Personalized Recommendations**: Get suggestions based on your interests

## 🏗️ Architecture

Built with:
- **LangGraph**: Agent orchestration and state management
- **Langmem**: Long-term memory with semantic search
- **Claude Sonnet 4.5**: Advanced reasoning and natural language understanding
- **GitHub Data**: Real-time scraping + REST API integration

## 📦 Installation

### Prerequisites

- Python 3.9+
- Docker (for LangGraph Platform)
- API Keys: Anthropic, OpenAI

### Quick Start

1. **Install LangGraph CLI**:
```bash
pip install -U "langgraph-cli[inmem]"
```

2. **Clone/Download this project**

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the development server**:
```bash
langgraph dev
```

The agent will be available at:
- **API**: http://localhost:2024
- **LangGraph Studio**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## 🎮 Usage

### Using LangGraph Studio

1. Open LangGraph Studio (link shown when you run `langgraph dev`)
2. Start chatting with the agent:
   - "What are the trending Python repositories today?"
   - "Find machine learning projects"
   - "Remember that I prefer Rust and Go"
   - "Show me hot new repos from this week"

### Using Python SDK

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:2024")

# Start a conversation
async for chunk in client.runs.stream(
    None,  # Threadless run
    "github_trending_agent",  # Assistant name from langgraph.json
    input={
        "messages": [{
            "role": "user",
            "content": "What are the trending Python repos?"
        }]
    },
):
    print(chunk.data)
```

### Using REST API

```bash
curl -X POST http://localhost:2024/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "github_trending_agent",
    "input": {
      "messages": [{
        "role": "user",
        "content": "Find trending Rust projects"
      }]
    }
  }'
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

### 4. Memory Tools (Langmem)
- **Preferences**: Stores user preferences, favorite languages, topics
- **History**: Tracks search history and viewed repositories

## 📊 Project Structure

```
.
├── langgraph.json          # LangGraph configuration
├── pyproject.toml          # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
└── src/
    └── agent.py            # Main agent implementation
```

## 🔧 Configuration

### langgraph.json

```json
{
  "$schema": "https://langgra.ph/schema.json",
  "dependencies": ["."],
  "graphs": {
    "github_trending_agent": "./src/agent.py:graph"
  },
  "env": ".env",
  "store": {
    "index": {
      "embed": "openai:text-embedding-3-small",
      "dims": 1536
    }
  }
}
```

Key configurations:
- **graphs**: Defines the agent entry point
- **env**: Points to environment variables file
- **store.index**: Configures semantic search for memory

## 🧠 Memory System

The agent uses Langmem with two memory namespaces:

### User Preferences
Stores:
- Preferred programming languages
- Topics of interest
- Experience level
- Search patterns

### Search History
Stores:
- Past queries
- Viewed repositories
- Interaction patterns
- Feedback

Memory is persisted using LangGraph's built-in store with semantic search enabled.

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
Agent: [Stores preference in memory]

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
langgraph dev
```

### Production Deployment

1. **Build Docker image**:
```bash
langgraph build -t github-trending-agent:latest
```

2. **Deploy to LangGraph Cloud**:
```bash
langgraph deploy
```

Or deploy to any Docker-compatible platform.

## 📝 Development

### Run locally without LangGraph Platform
```bash
python src/agent.py
```

### Modify the agent
Edit `src/agent.py` to:
- Add new tools
- Customize system prompt
- Adjust model parameters
- Extend memory capabilities

### Hot reloading
`langgraph dev` automatically reloads on file changes.

## 🐛 Troubleshooting

### Issue: "langgraph: command not found"
**Solution**: Install LangGraph CLI: `pip install -U "langgraph-cli[inmem]"`

### Issue: "API key not found"
**Solution**: Ensure `.env` file exists with valid API keys

### Issue: "Rate limit exceeded"
**Solution**: Add GitHub token to `.env` for higher limits (60 → 5000 req/hour)

### Issue: "Module not found"
**Solution**: Ensure all dependencies are installed: `pip install -e .`

## 📚 Learn More

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangGraph Platform**: https://docs.langchain.com/langgraph-platform/
- **Langmem**: https://langchain-ai.github.io/langmem/
- **Claude API**: https://docs.anthropic.com/
- **GitHub API**: https://docs.github.com/en/rest

## 🎯 Key LangGraph Concepts

### State Management
The agent uses `MessagesState` for conversation management with automatic message persistence.

### Tool Calling
Tools are decorated with `@tool` and automatically integrated into the agent workflow.

### Conditional Edges
The graph uses `tools_condition` to dynamically route between agent and tool execution.

### Checkpointing
`MemorySaver` provides conversation persistence across sessions.

### Memory Store
LangGraph's built-in store with semantic search for intelligent memory retrieval.

## 🤝 Contributing

This is a reference implementation. Feel free to:
- Add more GitHub data sources (GitLab, Bitbucket)
- Implement code analysis features
- Add visualization tools
- Build custom UI
- Extend memory capabilities

## 📄 License

MIT License - Use freely in your projects!

## 🙏 Acknowledgments

- **Anthropic** for Claude
- **LangChain team** for LangGraph and Langmem
- **GitHub** for trending data
- **Open source community**

---

**Built with ❤️ using LangGraph Platform**

For issues or questions, please refer to:
- [LangGraph Discussions](https://github.com/langchain-ai/langgraph/discussions)
- [LangChain Discord](https://discord.gg/langchain)
