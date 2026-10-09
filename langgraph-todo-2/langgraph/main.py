"""
Main entry point for the Todo Agent CLI
"""

import os
import sys
from agent.todo_agent import create_todo_agent


def main():
    """Main function to run the Todo Agent CLI"""
    
    # Check for Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: Please set your GROQ_API_KEY environment variable")
        print("   Example: export GROQ_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    try:
        # Create the agent
        agent = create_todo_agent()
        
        print("🚀 Todo Management Agent is ready!")
        print("="*50)
        print("📋 Available Commands:")
        print("  👥 USER MANAGEMENT:")
        print("    • Create user: 'Create a user named John with email john@example.com'")
        print("    • List users: 'Show me all users' or 'List users'")
        print("    • User info: 'Tell me about user_1'")
        print("")
        print("  📋 TASK MANAGEMENT:")
        print("    • Create task: 'Create a task called Setup Project with description Set up the new project'")
        print("    • Assign task: 'Assign task_1 to user_1'")
        print("    • Update status: 'Update task_1 status to in_progress'")
        print("    • List tasks: 'List all tasks' or 'Show me all tasks'")
        print("    • Task info: 'Tell me about task_1'")
        print("")
        print("  💡 GENERAL:")
        print("    • Help: 'What can you do?' or 'Help me'")
        print("    • Stats: 'Show me system stats'")
        print("")
        print("  🚪 EXIT:")
        print("    • Type 'quit', 'exit', or 'bye' to exit")
        print("="*50)
        
        # Show initial stats
        stats = agent.get_system_stats()
        print(f"📊 Current Status: {stats['total_users']} users, {stats['total_tasks']} tasks")
        print("")
        
        # Main chat loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye! Have a great day!")
                    break
                
                if not user_input:
                    continue
                
                # Special commands
                if user_input.lower() in ['stats', 'status', 'show stats']:
                    stats = agent.get_system_stats()
                    print("📊 System Statistics:")
                    print(f"  👥 Total Users: {stats['total_users']}")
                    print(f"  📋 Total Tasks: {stats['total_tasks']}")
                    print(f"  ⏳ Pending: {stats['pending_tasks']}")
                    print(f"  🔄 In Progress: {stats['in_progress_tasks']}")
                    print(f"  ✅ Completed: {stats['completed_tasks']}")
                    print(f"  👤 Unassigned: {stats['unassigned_tasks']}")
                    continue
                
                if user_input.lower() in ['clear', 'reset']:
                    confirm = input("⚠️  Are you sure you want to clear all data? (yes/no): ")
                    if confirm.lower() in ['yes', 'y']:
                        agent.clear_all_data()
                        print("✅ All data cleared successfully!")
                    else:
                        print("❌ Operation cancelled.")
                    continue
                
                if user_input.lower() in ['export']:
                    data = agent.export_data()
                    print("💾 Current Data Export:")
                    print(f"Users: {len(data['users'])}")
                    print(f"Tasks: {len(data['tasks'])}")
                    # You could save this to a file if needed
                    continue
                
                # Chat with the agent
                response = agent.chat(user_input)
                print(f"🤖 Agent: {response}")
                print("")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()