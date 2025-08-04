import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

tasks = []
filename = "tasks.json"

# ----------------- File Functions -----------------
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

# ----------------- GUI Functions -----------------
def refresh_listbox():
    task_list.delete(*task_list.get_children())
    for i, task in enumerate(tasks):
        task_list.insert("", "end", values=(task["subject"], task["description"], task["due"]))

def add_task():
    def submit():
        subject = subject_entry.get().strip()
        description = desc_entry.get().strip()
        due = due_entry.get().strip()

        if not subject or not description or not due:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        task = {"subject": subject, "description": description, "due": due}
        tasks.append(task)
        save_tasks()
        refresh_listbox()
        popup.destroy()

    def cancel():
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("➕ Add New Task")
    popup.geometry("400x250")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    label_font = ("Segoe UI", 10, "bold")
    entry_font = ("Segoe UI", 10)

    tk.Label(popup, text="Subject", bg="#1e1e1e", fg="white", font=label_font).pack(pady=(10, 0))
    subject_entry = tk.Entry(popup, font=entry_font, bg="#2e2e2e", fg="white", insertbackground="white")
    subject_entry.pack(padx=20, fill="x")

    tk.Label(popup, text="Description", bg="#1e1e1e", fg="white", font=label_font).pack(pady=(10, 0))
    desc_entry = tk.Entry(popup, font=entry_font, bg="#2e2e2e", fg="white", insertbackground="white")
    desc_entry.pack(padx=20, fill="x")

    tk.Label(popup, text="Due Date", bg="#1e1e1e", fg="white", font=label_font).pack(pady=(10, 0))
    due_entry = tk.Entry(popup, font=entry_font, bg="#2e2e2e", fg="white", insertbackground="white")
    due_entry.pack(padx=20, fill="x")

    btn_frame = tk.Frame(popup, bg="#1e1e1e")
    btn_frame.pack(pady=15)

    ttk.Button(btn_frame, text="Add Task", command=submit, style="Big.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Cancel", command=cancel, style="Big.TButton").grid(row=0, column=1, padx=10)

def delete_task():
    selected = task_list.selection()
    if not selected:
        messagebox.showwarning("Delete Task", "Please select a task to delete.")
        return
    index = task_list.index(selected[0])
    deleted = tasks.pop(index)
    save_tasks()
    refresh_listbox()
    messagebox.showinfo("Deleted", f"🗑️ Deleted: {deleted['description']}")

# ----------------- Main GUI Setup -----------------
load_tasks()

root = tk.Tk()
root.title("📚 Homework Tracker")
root.geometry("700x400")
root.configure(bg="#1e1e1e")  # Dark background

# ----------------- Dark Theme Style -----------------
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#1e1e1e",
    foreground="white",
    rowheight=30,
    fieldbackground="#1e1e1e",
    font=("Segoe UI", 10)
)
style.configure("Treeview.Heading",
    background="#007acc",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)
style.map("Treeview",
    background=[("selected", "#333333")],
    foreground=[("selected", "white")]
)

style.configure("Big.TButton",
    font=("Segoe UI", 12, "bold"),
    padding=10,
    background="#333333",
    foreground="white"
)
style.map("Big.TButton",
    background=[("active", "#005f99")]
)

task_list = ttk.Treeview(root, columns=("Subject", "Description", "Due"), show="headings", style="Treeview")
task_list.heading("Subject", text="Subject")
task_list.heading("Description", text="Description")
task_list.heading("Due", text="Due Date")
task_list.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(task_list, orient="vertical", command=task_list.yview)
task_list.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

add_btn = ttk.Button(btn_frame, text="➕ Add Task", command=add_task, style="Big.TButton")
add_btn.grid(row=0, column=0, padx=15, ipadx=20, ipady=10)

delete_btn = ttk.Button(btn_frame, text="🗑️ Delete Task", command=delete_task, style="Big.TButton")
delete_btn.grid(row=0, column=1, padx=15, ipadx=20, ipady=10)

exit_btn = ttk.Button(btn_frame, text="❌ Exit", command=root.quit, style="Big.TButton")
exit_btn.grid(row=0, column=2, padx=15, ipadx=20, ipady=10)

refresh_listbox()
root.mainloop()
