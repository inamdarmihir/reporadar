"""
GitHub Trending Agent - Streamlit UI
Single-file application with Agno framework and beautiful GitHub results display
"""

import streamlit as st
from typing import List, Dict, Any
from agno import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GitHub Trending Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .repo-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .repo-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .repo-desc {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    .repo-stats {
        display: flex;
        gap: 1.5rem;
        font-size: 0.9rem;
    }
    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background: #e3f2fd;
        margin-left: 2rem;
    }
    .agent-message {
        background: #f3e5f5;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# GITHUB DATA FETCHING
# ============================================================================

class GitHubTrendingScraper:
    """Scraper for GitHub trending repositories"""
    
    @staticmethod
    def scrape_trending(
        language: str | None = None,
        since: str = "daily"
    ) -> List[Dict[str, Any]]:
        """Scrape GitHub trending page"""
        base_url = "https://github.com/trending"
        url = f"{base_url}/{language}" if language else base_url
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(
                url,
                params={"since": since},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            repos = []
            
            articles = soup.find_all('article', class_='Box-row')
            
            for idx, article in enumerate(articles, 1):
                try:
                    h2 = article.find('h2')
                    if not h2:
                        continue
                    
                    repo_link = h2.find('a')
                    if not repo_link:
                        continue
                    
                    full_name = repo_link.get('href', '').strip('/')
                    parts = full_name.split('/')
                    if len(parts) != 2:
                        continue
                    author, name = parts
                    
                    desc_elem = article.find('p')
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    lang_elem = article.find('span', attrs={"itemprop": "programmingLanguage"})
                    language_found = lang_elem.text.strip() if lang_elem else "Unknown"
                    
                    star_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
                    stars_text = star_elem.text.strip() if star_elem else "0"
                    stars = GitHubTrendingScraper._parse_number(stars_text)
                    
                    fork_elem = article.find('a', href=lambda x: x and 'forks' in x)
                    forks_text = fork_elem.text.strip() if fork_elem else "0"
                    forks = GitHubTrendingScraper._parse_number(forks_text)
                    
                    stars_period_elem = article.find('span', class_='d-inline-block float-sm-right')
                    stars_period_text = stars_period_elem.text.strip() if stars_period_elem else "0 stars"
                    stars_period = GitHubTrendingScraper._parse_number(stars_period_text.split()[0])
                    
                    repos.append({
                        "rank": idx,
                        "author": author,
                        "name": name,
                        "full_name": full_name,
                        "url": f"https://github.com/{full_name}",
                        "description": description,
                        "language": language_found,
                        "stars": stars,
                        "forks": forks,
                        "stars_period": stars_period,
                        "since": since
                    })
                    
                except Exception:
                    continue
            
            return repos
            
        except Exception as e:
            st.error(f"Error scraping GitHub trending: {e}")
            return []
    
    @staticmethod
    def _parse_number(text: str) -> int:
        """Parse number from text like '1.2k' or '1,234'"""
        text = text.replace(',', '').strip()
        if 'k' in text.lower():
            return int(float(text.lower().replace('k', '')) * 1000)
        elif 'm' in text.lower():
            return int(float(text.lower().replace('m', '')) * 1000000)
        try:
            return int(float(text))
        except:
            return 0


class GitHubAPIClient:
    """GitHub REST API client"""
    
    def __init__(self, token: str | None = None):
        self.token = token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        per_page: int = 10
    ) -> List[Dict[str, Any]]:
        """Search repositories via GitHub API"""
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": "desc",
            "per_page": per_page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            st.error(f"Error searching repos: {e}")
            return []


# ============================================================================
# TOOLS
# ============================================================================

@tool
def get_trending_repos(language: str = "", time_period: str = "daily") -> str:
    """Get trending GitHub repositories"""
    scraper = GitHubTrendingScraper()
    lang = language if language else None
    repos = scraper.scrape_trending(language=lang, since=time_period)
    
    # Store in session state for display
    st.session_state.github_results = repos
    st.session_state.result_type = "trending"
    
    if not repos:
        return f"No trending repositories found for {language or 'all languages'} ({time_period})."
    
    result = f"Found {len(repos)} trending {language or 'all language'} repositories ({time_period})"
    return result


@tool
def search_repos(query: str, max_results: int = 10) -> str:
    """Search GitHub repositories using natural language"""
    github_token = os.getenv("GITHUB_TOKEN", "")
    client = GitHubAPIClient(token=github_token)
    max_results = min(max(1, max_results), 10)
    repos_raw = client.search_repositories(query, per_page=max_results)
    
    # Convert to display format
    repos = []
    for idx, repo in enumerate(repos_raw, 1):
        repos.append({
            "rank": idx,
            "author": repo['owner']['login'],
            "name": repo['name'],
            "full_name": repo['full_name'],
            "url": repo['html_url'],
            "description": repo.get('description', ''),
            "language": repo.get('language', 'Unknown'),
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
        })
    
    # Store in session state for display
    st.session_state.github_results = repos
    st.session_state.result_type = "search"
    
    if not repos:
        return f"No repositories found matching: '{query}'"
    
    return f"Found {len(repos)} repositories matching '{query}'"


@tool
def get_hot_repos(language: str = "", days: int = 7) -> str:
    """Get hot new repositories created recently"""
    github_token = os.getenv("GITHUB_TOKEN", "")
    client = GitHubAPIClient(token=github_token)
    days = min(max(1, days), 30)
    
    date_threshold = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    query = f"created:>{date_threshold}"
    if language:
        query += f" language:{language}"
    
    repos_raw = client.search_repositories(query, sort="stars", per_page=10)
    
    # Convert to display format
    repos = []
    for idx, repo in enumerate(repos_raw, 1):
        repos.append({
            "rank": idx,
            "author": repo['owner']['login'],
            "name": repo['name'],
            "full_name": repo['full_name'],
            "url": repo['html_url'],
            "description": repo.get('description', ''),
            "language": repo.get('language', 'Unknown'),
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "created_at": repo['created_at'][:10]
        })
    
    # Store in session state for display
    st.session_state.github_results = repos
    st.session_state.result_type = "hot"
    
    if not repos:
        return f"No hot repositories found for {language or 'all languages'} in last {days} days."
    
    return f"Found {len(repos)} hot new repositories from the last {days} days"


# ============================================================================
# AGENT SETUP
# ============================================================================

SYSTEM_INSTRUCTIONS = """You are an expert GitHub repository discovery assistant.

**Your capabilities:**
1. Fetch trending repositories (daily/weekly/monthly) across all programming languages
2. Search repositories using natural language queries
3. Find hot new repositories from recent days
4. Remember user preferences and provide personalized recommendations

**Best practices:**
- Be concise and helpful
- Use the tools to fetch real GitHub data
- Explain what you're showing the user
- Suggest related searches when appropriate

Be helpful and accurate in every interaction!"""


@st.cache_resource
def create_github_agent() -> Agent:
    """Create and configure the GitHub Trending Agent"""
    agent = Agent(
        name="GitHub Trending Agent",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[get_trending_repos, search_repos, get_hot_repos],
        instructions=SYSTEM_INSTRUCTIONS,
        storage=SqliteAgentStorage(
            table_name="github_agent_sessions",
            db_file="tmp/agent_storage.db"
        ),
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True,
        show_tool_calls=False,
        debug_mode=False,
    )
    return agent


# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_repo_card(repo: Dict[str, Any]):
    """Display a beautiful repository card"""
    with st.container():
        st.markdown(f"""
        <div class="repo-card">
            <div class="repo-title">#{repo['rank']} {repo['full_name']}</div>
            <div class="repo-desc">{repo.get('description', 'No description available')[:200]}</div>
            <div class="repo-stats">
                <div class="stat-item">⭐ {repo['stars']:,} stars</div>
                <div class="stat-item">🔱 {repo.get('forks', 0):,} forks</div>
                <div class="stat-item">💻 {repo['language']}</div>
                {f"<div class='stat-item'>📅 Created: {repo['created_at']}</div>" if 'created_at' in repo else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.link_button("🔗 View on GitHub", repo['url'], use_container_width=True)


def display_github_results():
    """Display GitHub results if available"""
    if 'github_results' in st.session_state and st.session_state.github_results:
        st.markdown("---")
        st.markdown("### 📊 GitHub Results")
        
        for repo in st.session_state.github_results[:10]:
            display_repo_card(repo)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 GitHub Trending Agent</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Discover trending repositories with AI-powered natural language search</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            help="Enter your Anthropic API key"
        )
        
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        
        github_token = st.text_input(
            "GitHub Token (Optional)",
            type="password",
            value=os.getenv("GITHUB_TOKEN", ""),
            help="Optional: Increases rate limits from 60 to 5000 req/hour"
        )
        
        if github_token:
            os.environ["GITHUB_TOKEN"] = github_token
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("🔥 Trending Python", use_container_width=True):
            st.session_state.quick_query = "Show me trending Python repositories today"
        
        if st.button("🚀 Hot New Repos", use_container_width=True):
            st.session_state.quick_query = "Find hot new repositories from the last 7 days"
        
        if st.button("🤖 ML Projects", use_container_width=True):
            st.session_state.quick_query = "Search for popular machine learning projects"
        
        if st.button("🌐 Web Frameworks", use_container_width=True):
            st.session_state.quick_query = "Find trending web frameworks"
        
        st.markdown("---")
        st.markdown("### 📚 Examples")
        st.markdown("""
        - "Trending Python repos today"
        - "Hot Rust projects last week"
        - "Search for AI frameworks"
        - "Show me TypeScript tools"
        """)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'github_results' not in st.session_state:
        st.session_state.github_results = []
    
    # Check for API key
    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API Key in the sidebar to get started!")
        st.info("💡 Get your API key from: https://console.anthropic.com/")
        return
    
    # Create agent
    try:
        agent = create_github_agent()
    except Exception as e:
        st.error(f"Error creating agent: {e}")
        return
    
    # Chat interface
    st.markdown("### 💬 Chat with the Agent")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle quick query
    if 'quick_query' in st.session_state:
        user_input = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        user_input = st.chat_input("Ask about GitHub repositories...")
    
    # Process user input
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response: RunResponse = agent.run(user_input, stream=False)
                    assistant_message = response.content
                    
                    st.markdown(assistant_message)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Display GitHub results
        display_github_results()
        
        # Auto-rerun to show results
        st.rerun()
    
    # Display existing results if any
    elif 'github_results' in st.session_state and st.session_state.github_results:
        display_github_results()


if __name__ == "__main__":
    main()
