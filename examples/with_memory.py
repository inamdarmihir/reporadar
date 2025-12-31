"""
Memory Example - GitHub Trending Agent with Agno
Demonstrates how the agent remembers preferences across sessions
"""

from app import agent

def main():
    print("🧠 GitHub Trending Agent - Memory & Personalization Examples\n")
    print("=" * 80)
    
    # Use a consistent session ID to maintain memory
    session_id = "demo-session-001"
    
    # Example 1: Set preferences
    print("\n💾 Example 1: Setting User Preferences")
    print("-" * 80)
    response = agent.run(
        "Remember that I prefer Python and TypeScript for web development, and I'm interested in AI/ML projects",
        stream=False,
        session_id=session_id
    )
    print(response.content)
    
    # Example 2: Get personalized recommendations
    print("\n" + "=" * 80)
    print("\n🎯 Example 2: Personalized Recommendations")
    print("-" * 80)
    response = agent.run(
        "What's trending this week that I might like?",
        stream=False,
        session_id=session_id
    )
    print(response.content)
    
    # Example 3: Recall preferences
    print("\n" + "=" * 80)
    print("\n🔍 Example 3: Recalling Preferences")
    print("-" * 80)
    response = agent.run(
        "What do you remember about my preferences?",
        stream=False,
        session_id=session_id
    )
    print(response.content)
    
    # Example 4: Search based on interests
    print("\n" + "=" * 80)
    print("\n🎨 Example 4: Interest-Based Search")
    print("-" * 80)
    response = agent.run(
        "Find some new projects in my favorite languages",
        stream=False,
        session_id=session_id
    )
    print(response.content)
    
    print("\n" + "=" * 80)
    print("\n✅ Memory examples completed!")
    print(f"📝 Session ID: {session_id}")
    print("💡 The agent will remember these preferences in future conversations with this session ID")

if __name__ == "__main__":
    main()
