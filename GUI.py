import tkinter as tk
from tkinter import messagebox

from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule


class GraphicalUserInterface:
    def __init__(self):
        self.nlpm = NaturalLanguageProcessingModule()
        self.cem = CommandExecutionModule()

        self.root = tk.Tk()
        self.root.title("Speech Assistant GUI")
        self.root.geometry("450x180")
        self.root.resizable(False, False)

        self._build_widgets()

    def _build_widgets(self):
        label = tk.Label(self.root, text="Enter a text command:", font=("Arial", 12))
        label.pack(pady=(20, 8))

        self.command_var = tk.StringVar()
        entry = tk.Entry(self.root, textvariable=self.command_var, width=50, font=("Arial", 11))
        entry.pack(padx=16)
        entry.focus()

        execute_button = tk.Button(self.root, text="Execute", command=self.on_submit, width=12, font=("Arial", 11))
        execute_button.pack(pady=20)

    def on_submit(self):
        command = self.command_var.get().strip()

        if not command:
            messagebox.showwarning("Input required", "Please enter a command before executing.")
            return

        intent = self.nlpm.recognize_intent(command)
        query = command if intent == "search_google" else None
        success = self.cem.execute(intent, query)

        if success:
            message = f"Recognized intent: {intent}\nAction executed successfully."
        else:
            message = f"Recognized intent: {intent}\nThe command could not be completed."

        messagebox.showinfo("Command Result", message)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GraphicalUserInterface().run()
