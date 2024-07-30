import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import itertools
import threading
import time

class NumberGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NumberGenerator")
        
        self.label_input = tk.Label(root, text="First input number:")
        self.label_input.grid(row=0, column=0, pady=5)
        
        self.entry_input = tk.Entry(root, width=20)
        self.entry_input.grid(row=0, column=1, pady=5, columnspan=2)
        
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=self.progress)
        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=5)

        self.progress_label = tk.Label(root, text="0%")
        self.progress_label.grid(row=3, column=3, padx=5)
        
        self.generate_button = tk.Button(root, text="Confirm", command=self.start_generation)
        self.generate_button.grid(row=4, column=0, padx=5, pady=12)
        
        self.save_button = tk.Button(root, text="Save", command=self.save_numbers)
        self.save_button.grid(row=4, column=1, padx=5, pady=12)
        
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_selected)
        self.delete_button.grid(row=4, column=2, padx=5, pady=12)
        
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.listbox.grid(row=2, column=0, columnspan=3, pady=5, padx=8, sticky="nsew")
        
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=3, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Adjust grid weights for resizing behavior
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(2, weight=1)
        
    def start_generation(self):
        threading.Thread(target=self.generate_numbers).start()

    def generate_numbers(self):
        pattern = self.entry_input.get()
        if not pattern:
            messagebox.showwarning("Invalid input", "Please enter an input number")
            return

        stars_count = pattern.count('*')
        total_combinations = 10 ** stars_count

        self.listbox.delete(0, tk.END)
        self.progress.set(0)
        step = 100 / total_combinations

        for i, combo in enumerate(itertools.product('0123456789', repeat=stars_count)):
            number = pattern
            for digit in combo:
                number = number.replace('*', digit, 1)
            self.listbox.insert(tk.END, number)
            self.progress.set(self.progress.get() + step)
            self.progress_label.config(text=f"{int(self.progress.get())}%")
            time.sleep(0.001)  # Add a small delay to keep the UI responsive

        self.progress.set(100)
        self.progress_label.config(text="100%")

    def save_numbers(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        with open(file_path, "w") as file:
            for number in self.listbox.get(0, tk.END):
                file.write(number + "\n")
        messagebox.showinfo("Saved", "Numbers saved successfully")

    def delete_selected(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        self.listbox.delete(selected_indices[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGeneratorApp(root)
    root.mainloop()
