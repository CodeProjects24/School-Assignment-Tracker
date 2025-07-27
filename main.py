import json
import os

tasks = []
filename = "tasks.json"

def load_tasks():
    global tasks
    if os.path.exists(filename):
        with open(filename, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

def save_tasks():
    with open(filename, "w") as f:
        json.dump(tasks, f)

def show_menu():
    print("\n📚 Homework Tracker")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark task as done")
    print("4. Exit")

def add_task():
    subject = input("Subject: ")
    description = input("Task description: ")
    due = input("Due date (e.g., July 30): ")
    task = {
        "subject": subject,
        "description": description,
        "due": due,
        "done": False
    }
    tasks.append(task)
    save_tasks()
    print("✅ Task added!")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return
    for i, task in enumerate(tasks):
        status = "✅ Done" if task["done"] else "❌ Not done"
        print(f"\nTask {i + 1}")
        print(f"Subject: {task['subject']}")
        print(f"Description: {task['description']}")
        print(f"Due: {task['due']}")
        print(f"Status: {status}")

def mark_done():
    view_tasks()
    if not tasks:
        return
    try:
        index = int(input("Enter task number to mark as done: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks()
            print("✅ Task marked as done!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Load saved tasks
load_tasks()

# Main loop
while True:
    show_menu()
    choice = input("Choose an option (1–4): ")
    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")

