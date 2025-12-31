# 🚀 GitHub Trending Agent - Streamlit UI

Beautiful Streamlit interface for discovering GitHub trending repositories using AI-powered natural language search.

## ✨ Features

- 🎨 **Beautiful UI**: Gradient cards, modern design
- 💬 **Chat Interface**: Natural language queries
- 🔍 **Real GitHub Data**: Live trending, search, and hot repos
- 🧠 **AI-Powered**: Agno framework with Claude Sonnet 4.5
- 🎯 **Quick Actions**: One-click trending searches
- 💾 **Memory**: Remembers your preferences

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Set Up API Keys

Create a `.env` file:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional
```

Or enter them directly in the Streamlit sidebar.

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 💡 Usage

### Quick Actions (Sidebar)
- Click any quick action button for instant results
- 🔥 Trending Python
- 🚀 Hot New Repos
- 🤖 ML Projects
- 🌐 Web Frameworks

### Natural Language Queries
Type any question in the chat:
- "Show me trending Python repositories today"
- "Find hot new Rust projects from the last 7 days"
- "Search for popular machine learning frameworks"
- "What are the trending TypeScript repos this week?"

### GitHub Results
- Beautiful gradient cards for each repository
- Stars, forks, language, and creation date
- Direct links to GitHub
- Automatic display after queries

## 🎨 UI Features

- **Gradient Cards**: Eye-catching repository displays
- **Responsive Layout**: Works on all screen sizes
- **Dark Mode Support**: Follows Streamlit theme
- **Quick Actions**: One-click common searches
- **Chat History**: See your conversation
- **Real-time Updates**: Live GitHub data

## 🔧 Configuration

### API Keys
- **Anthropic API Key** (Required): Get from https://console.anthropic.com/
- **GitHub Token** (Optional): Increases rate limits from 60 to 5000 req/hour

### Customization
Edit `streamlit_app.py` to:
- Change color schemes (CSS section)
- Modify quick action buttons
- Adjust number of results
- Customize agent instructions

## 📝 Example Queries

```
"Trending Python repos today"
"Hot Rust projects last week"
"Search for AI frameworks"
"Show me TypeScript tools"
"Find web development libraries"
"What's trending in Go this month?"
```

## 🛠️ Tools Available

1. **get_trending_repos**: Daily/weekly/monthly trending
2. **search_repos**: Natural language search
3. **get_hot_repos**: Recently created popular repos

## 📦 Single File

Everything is in one file: `streamlit_app.py`
- Agent setup
- GitHub scraping
- API integration
- UI components
- Chat interface

## 🚀 Deployment

Deploy to Streamlit Cloud:

1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repo
4. Add secrets (API keys)
5. Deploy!

## 📄 License

MIT License - Use freely!

---

**Built with ❤️ using Agno + Streamlit**
