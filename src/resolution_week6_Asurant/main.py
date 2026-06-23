import tkinter as tk
from tkinter import messagebox
import json, os

TASKS_FILE = "tasks.json"

def main():
    def load_tasks():
        if not os.path.exists(TASKS_FILE):
            return []
        with open(TASKS_FILE, "r") as f:
            return json.load(f)

    def save_tasks(tasks):
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)

    def add_task():
        task = inputTask.get()
        if len(tasks) == 0:
            new_id = 1
        else:
            new_id = tasks[-1]["id"]+1

        tasks.append({"id": new_id, "task": task, "done": False})
        save_tasks(tasks)
        
        refresh_listbox()

    def toggle_complete():
        select = tasksListbox.curselection()

        if not select:
            return

        index = select[0]

        tasks[index]["done"] = not tasks[index]["done"]

        save_tasks(tasks)
        
        refresh_listbox()


    def toggle_delete():
        select = tasksListbox.curselection()
        
        if not select:
            return
        
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            tasks.pop(select[0])
            save_tasks(tasks)
            refresh_listbox()

    def clear_completed():
        if messagebox.askyesno("Clear Completed Tasks", "Are you sure you want to delete all completed tasks?"):
            for i in range(len(tasks) -1, -1, -1):
                if tasks[i]["done"]:
                    tasks.pop(i)
            save_tasks(tasks)
            refresh_listbox()

    def update_stats():
        completed = 0
        for task in tasks:
            if task["done"]:
                completed+=1
        completedTasksLabel.config(text = f"Completed {completed} tasks out of {len(tasks)}")

    def refresh_listbox():
        tasksListbox.delete(0, tk.END)

        for task in tasks:
            if task["done"]:
                tasksListbox.insert(tk.END, "[X]" + task["task"])
            else:
                tasksListbox.insert(tk.END, "[ ]" + task["task"])
        
        update_stats()

    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x300")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight = 1)

    inputFrame = tk.Frame(root)
    inputFrame.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
    inputFrame.columnconfigure(0, weight = 1)

    inputTask = tk.Entry(inputFrame)
    inputTask.grid(row = 0, column = 0, sticky= "ew", padx=(5, 5))

    addTask = tk.Button(inputFrame, text = "Add Task", command=add_task)
    addTask.grid(row = 0, column=1, padx= 5)


    tasksFrame = tk.Frame(root)
    tasksFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 5, pady = 5)
    tasksFrame.columnconfigure(0, weight = 1)
    tasksFrame.rowconfigure(0, weight = 1)


    tasksScrollbar = tk.Scrollbar(tasksFrame)
    tasksScrollbar.grid(row = 0, column=1, sticky="ns")

    tasksListbox = tk.Listbox(tasksFrame, yscrollcommand=tasksScrollbar.set)
    tasksListbox.grid(row = 0, column = 0, sticky = "nsew", padx = 5, pady = 5)

    tasksScrollbar.config(command=tasksListbox.yview)

    buttonsFrame = tk.Frame(root)
    buttonsFrame.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)
    buttonsFrame.columnconfigure(0, weight = 1)
    buttonsFrame.columnconfigure(1, weight = 1)
    buttonsFrame.columnconfigure(2, weight = 1)

    completeButton = tk.Button(buttonsFrame, text="Complete", command=toggle_complete)
    completeButton.grid(row = 0, column = 0, sticky= "ew", padx=5)

    deleteButton = tk.Button(buttonsFrame, text="Delete", command=toggle_delete)
    deleteButton.grid(row = 0, column = 1, sticky= "ew", padx=5)

    clearButton = tk.Button(buttonsFrame, text = "Clear All Completed", command=clear_completed)
    clearButton.grid(row = 0, column = 2, sticky= "ew", padx=5)

    statsFrame = tk.Frame(root)
    statsFrame.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 5)

    statsFrame.columnconfigure(0, weight = 1)

    statsTitleLabel = tk.Label(statsFrame, text="Stats", font=(18), anchor="center")
    statsTitleLabel.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

    completedTasksLabel = tk.Label(statsFrame, text="Completed 0 tasks out of 0")
    completedTasksLabel.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)

    tasks = load_tasks()
    refresh_listbox()

    root.mainloop()

if __name__ == "__main__":
    main()