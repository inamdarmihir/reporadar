"""
Basic Usage Example - GitHub Trending Agent with Agno
Demonstrates simple queries to the agent
"""

from app import agent

def main():
    print("🚀 GitHub Trending Agent - Basic Usage Examples\n")
    print("=" * 80)
    
    # Example 1: Get trending Python repos
    print("\n📊 Example 1: Trending Python Repositories")
    print("-" * 80)
    response = agent.run("What are the trending Python repositories today?", stream=False)
    print(response.content)
    
    # Example 2: Search for machine learning projects
    print("\n" + "=" * 80)
    print("\n🔍 Example 2: Search for Machine Learning Projects")
    print("-" * 80)
    response = agent.run("Find popular machine learning frameworks", stream=False)
    print(response.content)
    
    # Example 3: Hot new repos
    print("\n" + "=" * 80)
    print("\n🔥 Example 3: Hot New Repositories")
    print("-" * 80)
    response = agent.run("Show me hot new repos from the last 7 days in Rust", stream=False)
    print(response.content)
    
    print("\n" + "=" * 80)
    print("\n✅ Examples completed!")

if __name__ == "__main__":
    main()
