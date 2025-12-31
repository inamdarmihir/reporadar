"""
GitHub Trending Agent - Agno Framework Implementation
A production-ready agent for discovering GitHub trending repositories using natural language.
"""

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

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


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
                    
                    # Description
                    desc_elem = article.find('p')
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    # Language
                    lang_elem = article.find('span', attrs={"itemprop": "programmingLanguage"})
                    language_found = lang_elem.text.strip() if lang_elem else "Unknown"
                    
                    # Stars
                    star_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
                    stars_text = star_elem.text.strip() if star_elem else "0"
                    stars = GitHubTrendingScraper._parse_number(stars_text)
                    
                    # Forks
                    fork_elem = article.find('a', href=lambda x: x and 'forks' in x)
                    forks_text = fork_elem.text.strip() if fork_elem else "0"
                    forks = GitHubTrendingScraper._parse_number(forks_text)
                    
                    # Stars today/this week/this month
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
                    
                except Exception as e:
                    continue
            
            return repos
            
        except Exception as e:
            print(f"Error scraping GitHub trending: {e}")
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
            print(f"Error searching repos: {e}")
            return []


# ============================================================================
# TOOLS
# ============================================================================

@tool
def get_trending_repos(language: str = "", time_period: str = "daily") -> str:
    """
    Get trending GitHub repositories.
    
    Args:
        language: Programming language filter (e.g., 'python', 'javascript', 'rust'). Leave empty for all languages.
        time_period: Time period - 'daily', 'weekly', or 'monthly'
    
    Returns:
        Formatted string with trending repositories
    """
    scraper = GitHubTrendingScraper()
    lang = language if language else None
    repos = scraper.scrape_trending(language=lang, since=time_period)
    
    if not repos:
        return f"No trending repositories found for {language or 'all languages'} ({time_period})."
    
    result = f"📈 **Trending GitHub Repositories**\n"
    result += f"Language: {language or 'All'} | Period: {time_period.capitalize()}\n\n"
    
    for repo in repos[:10]:
        result += f"**#{repo['rank']} {repo['full_name']}**\n"
        result += f"   🔗 {repo['url']}\n"
        if repo['description']:
            desc = repo['description'][:150] + "..." if len(repo['description']) > 150 else repo['description']
            result += f"   📝 {desc}\n"
        result += f"   💻 {repo['language']} | ⭐ {repo['stars']:,} stars (+{repo['stars_period']} {time_period})\n"
        result += f"   🔱 {repo['forks']:,} forks\n\n"
    
    return result


@tool
def search_repos(query: str, max_results: int = 5) -> str:
    """
    Search GitHub repositories using natural language.
    
    Args:
        query: Search query (e.g., "machine learning frameworks", "web development tools")
        max_results: Maximum number of results (1-10)
    
    Returns:
        Formatted string with search results
    """
    client = GitHubAPIClient(token=GITHUB_TOKEN)
    max_results = min(max(1, max_results), 10)
    repos = client.search_repositories(query, per_page=max_results)
    
    if not repos:
        return f"No repositories found matching: '{query}'"
    
    result = f"🔍 **Search Results for '{query}'**\n\n"
    
    for idx, repo in enumerate(repos, 1):
        result += f"**{idx}. {repo['full_name']}**\n"
        result += f"   🔗 {repo['html_url']}\n"
        desc = repo.get('description', 'No description')
        if desc and len(desc) > 150:
            desc = desc[:150] + "..."
        result += f"   📝 {desc}\n"
        result += f"   💻 {repo.get('language', 'N/A')} | "
        result += f"⭐ {repo['stargazers_count']:,} | "
        result += f"🔱 {repo['forks_count']:,}\n\n"
    
    return result


@tool
def get_hot_repos(language: str = "", days: int = 7) -> str:
    """
    Get hot new repositories created recently.
    
    Args:
        language: Programming language filter. Leave empty for all languages.
        days: Number of days to look back (1-30)
    
    Returns:
        Formatted string with hot new repositories
    """
    client = GitHubAPIClient(token=GITHUB_TOKEN)
    days = min(max(1, days), 30)
    
    date_threshold = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    query = f"created:>{date_threshold}"
    if language:
        query += f" language:{language}"
    
    repos = client.search_repositories(query, sort="stars", per_page=10)
    
    if not repos:
        return f"No hot repositories found for {language or 'all languages'} in last {days} days."
    
    result = f"🔥 **Hot New Repositories**\n"
    result += f"Created in last {days} days | Language: {language or 'All'}\n\n"
    
    for idx, repo in enumerate(repos, 1):
        result += f"**{idx}. {repo['full_name']}**\n"
        result += f"   🔗 {repo['html_url']}\n"
        desc = repo.get('description', 'No description')
        if desc and len(desc) > 150:
            desc = desc[:150] + "..."
        result += f"   📝 {desc}\n"
        result += f"   💻 {repo.get('language', 'N/A')} | ⭐ {repo['stargazers_count']:,}\n"
        result += f"   📅 Created: {repo['created_at'][:10]}\n\n"
    
    return result


# ============================================================================
# AGENT SETUP
# ============================================================================

# System instructions
SYSTEM_INSTRUCTIONS = """You are an expert GitHub repository discovery assistant with long-term memory capabilities.

**Your capabilities:**
1. Fetch trending repositories (daily/weekly/monthly) across all programming languages
2. Search repositories using natural language queries
3. Find hot new repositories from recent days
4. Remember user preferences (languages, topics, interests)
5. Track search history and provide personalized recommendations

**How to help users:**
- When users express preferences, remember them for future interactions
- Before searching, consider any relevant context from previous conversations
- Provide detailed, actionable repository information
- Suggest related repositories based on their interests
- Learn from their feedback and refine recommendations

**Best practices:**
- Always provide repository URLs so users can explore
- Highlight key metrics (stars, forks, activity level)
- Explain why a repository might be relevant to the user
- Be concise but informative
- Use clear formatting for readability

Be helpful, accurate, and personalized in every interaction!"""


def create_github_agent() -> Agent:
    """Create and configure the GitHub Trending Agent"""
    
    # Initialize agent with Claude Sonnet 4.5
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
        num_history_responses=5,
        markdown=True,
        show_tool_calls=True,
        debug_mode=False,
    )
    
    return agent


# Create the agent instance
agent = create_github_agent()


# For local testing
if __name__ == "__main__":
    print("🚀 GitHub Trending Agent - Agno Framework\n")
    print("=" * 80)
    
    # Test queries
    test_queries = [
        "What are the trending Python repositories today?",
        "Find machine learning projects",
        "Show me hot new repos from the last 7 days in Rust",
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        print("-" * 80)
        
        # Run the agent
        response: RunResponse = agent.run(query, stream=False)
        
        print(f"🤖 Agent: {response.content}")
        print("=" * 80)