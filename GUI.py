import threading
import tkinter as tk
from tkinter import messagebox

from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule
from commands import plugins
from conversation_context import ConversationContext


class GraphicalUserInterface:
    def __init__(self, on_close=None, context=None):
        self.nlpm = NaturalLanguageProcessingModule()
        self.cem = CommandExecutionModule()
        self.context = context if context is not None else ConversationContext()
        self._on_close = on_close

        self.root = tk.Tk()
        self.root.title("Speech Assistant GUI")
        self.root.geometry("450x180")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self._build_widgets()

    def _close(self):
        if self._on_close:
            self._on_close()
        self.root.destroy()

    def _build_widgets(self):
        label = tk.Label(self.root, text="Enter a text command:", font=("Arial", 12))
        label.pack(pady=(20, 8))

        self.command_var = tk.StringVar()
        entry = tk.Entry(self.root, textvariable=self.command_var, width=50, font=("Arial", 11))
        entry.pack(padx=16)
        entry.focus()

        self.execute_button = tk.Button(self.root, text="Execute", command=self.on_submit, width=12, font=("Arial", 11))
        self.execute_button.pack(pady=20)

    def _run_command(self, command):
        intent = self.nlpm.recognize_intent(command, self.context)
        success = self.cem.execute(intent, command, self.context)

        if success:
            plugin = plugins.get(intent)
            label = plugin.name if plugin else intent
            message = f"Recognized: {label}\nAction executed successfully."
        else:
            message = f"Recognized intent: {intent}\nThe command could not be completed."

        self.root.after(0, self._show_result, message)
        self.root.after(0, lambda: self.execute_button.config(state="normal"))

    def _show_result(self, message):
        messagebox.showinfo("Command Result", message)

    def on_submit(self):
        command = self.command_var.get().strip()

        if not command:
            messagebox.showwarning("Input required", "Please enter a command before executing.")
            return

        self.execute_button.config(state="disabled")
        threading.Thread(target=self._run_command, args=(command,), daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GraphicalUserInterface().run()
