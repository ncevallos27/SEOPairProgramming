"""
To-Do CLI App by Edson and Nico


TODO List:
    Python dictionary object of tasks:
    {
        id=hash value for each task : Task object,
        ...
    }
""" 

import uuid
import json
import os

TASK_FILE = 'tasks.json'

class Task:
    def __init__(self, task: str, completed=False, id=None):
        self._task = task
        self._completed = completed
        self._id = id if id else (uuid.uuid4().int % 10000) # generates unique 4 digit id (e.g. 5842)
    
    @property
    def task(self) -> str:
        return self._task
    
    @task.setter
    def task(self, new_task):
        if not isinstance(new_task, str):
            return ValueError("Task musk be a string.")
        self._task = new_task
    
    @property
    def completed(self) -> bool:
        return self._completed
    
    @completed.setter
    def completed(self, complete):
        if not isinstance(complete, bool):
            return ValueError("Completed value must be a boolean.")
        self._completed = complete
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id
    
    def __str__(self):
        if self.completed:
            return f"[x] ({self.id}) {self.task}"
        else:
            return f"[ ] ({self.id}) {self.task}"
    

class TODO_List:
    "{ id : task }"
    def __init__(self):
        self.todos = {}
    
    # Add a task to the list
    def add_task(self, task: Task) -> None:
        self.todos[task.id] = task
    
    # List all tasks in the To-Do list
    def list_tasks(self) -> None:
        for task in self.todos.values():
            print(task)
    
    # Delete a task by id
    def delete_task(self, id: int) -> Task:
        return self.todos.pop(id)

    def mark_complete(self, id: int) -> None:
        self.todos[id].completed = True

    # Export list to JSON file
    def export_list(self) -> None:
        temp_dict = {}
        for task in self.todos.values():
            temp_dict[task.id] = {"task": task.task, "completed": task.completed}
        with open(TASK_FILE, 'w') as file:
            json.dump(temp_dict, file, indent=2)
    
    # Import list to JSON file
    def import_list(self):
        if not os.path.exists(TASK_FILE):
            return {}
        with open(TASK_FILE, 'r') as file:
            raw = json.load(file)
            for task in raw.keys():
                self.add_task(Task(task=raw[task]['task'], completed=raw[task]['completed'], id=task))

    
import sys

def main():
    todo_list = TODO_List()
    todo_list.import_list()
    
    while True:
        
        
        todo_list.list_tasks()
        
        print("1: add task  2: delete task  3: mark complete    4: exit")
        
        try:
            user_input = int(input("Enter option: "))

            match user_input:
                case 1:
                    new_task = input("Enter task name: ")
                    todo_list.add_task(Task(new_task))
                    continue
                case 2:
                    task_to_delete_id = int(input("Enter task id: "))
                    todo_list.delete_task(task_to_delete_id)
                    continue
                case 3:
                    task_to_mark_id = int(input("Enter task id: "))
                    todo_list.mark_complete(task_to_mark_id)
                    continue
                case 4:
                    print("Saving list...")
                    todo_list.export_list()
                    sys.exit()
                case _:
                    print("err: invalid option, try again")
                    continue
        except ValueError:
            print("error: Please enter a valid option")

if __name__ == "__main__":
    main()