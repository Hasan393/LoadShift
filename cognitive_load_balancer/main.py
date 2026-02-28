# main.py
import time
import os
from monitor import ActivityMonitor
from analyzer import calculate_load
from agent import initialize_agent, delegate_task

def check_for_tasks():
    """Reads the next task from the pending task file."""
    task_path = "tasks/todo.txt"
    if os.path.exists(task_path):
        with open(task_path, "r") as f:
            task = f.read().strip()
        return task
    return None

def clear_task():
    """Clears the task file once completed."""
    with open("tasks/todo.txt", "w") as f:
        f.write("")

def save_completed_work(code):
    """Saves the AI's generated code to a new file."""
    timestamp = int(time.time())
    file_path = f"tasks/completed_task_{timestamp}.py"
    with open(file_path, "w") as f:
        f.write(code)
    print(f"✅ [SUCCESS] AI completed the task and saved to: {file_path}")

def main():
    print("🧠 Starting Cognitive-Load-Balancer...")
    
    # Initialize the LLM Agent
    try:
        agent_model = initialize_agent()
        print("🤖 Google Gemini Agent Ready.")
    except Exception as e:
        print(f"Failed to initialize Agent: {e}")
        return

    # Start tracking keystrokes in the background
    monitor = ActivityMonitor()
    monitor.start()
    print("⌨️  Monitoring keystrokes, pauses, and Git activity...")

    # Main assessment loop
    while True:
        time.sleep(15) # Check load every 15 seconds
        
        load_score = calculate_load(monitor)
        print(f"📊 Current Cognitive Load: {load_score:.1f}%")

        if load_score >= 80: # Threshold for being overwhelmed
            print("🚨 HIGH COGNITIVE LOAD DETECTED! You seem overwhelmed.")
            
            task = check_for_tasks()
            if task:
                print(f"📥 Found pending task: '{task[:50]}...'")
                print("⚡ Delegating to AI Agent. Take a deep breath and a sip of water...")
                
                # Let the AI do the work
                result_code = delegate_task(agent_model, task)
                save_completed_work(result_code)
                
                # Clear task and reset metrics to lower the load score
                clear_task()
                monitor.reset_metrics()
                print("🔄 Metrics reset. Resuming monitoring...\n")
            else:
                print("📭 No pending tasks in tasks/todo.txt to delegate. Take a break!")
                # Reset anyway to avoid spamming the terminal
                monitor.reset_metrics()

if __name__ == "__main__":
    main()