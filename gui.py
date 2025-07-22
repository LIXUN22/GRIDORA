import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Operations Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#f9f9f9")

        self.setup_ui()

    def setup_ui(self):
        # Header
        ttk.Label(self.root, text="Matrix Operations Tool", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # Matrix dimensions and operation
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack()

        ttk.Label(control_frame, text="Rows A").grid(row=0, column=0)
        self.rows_a = tk.IntVar(value=2)
        ttk.Entry(control_frame, textvariable=self.rows_a, width=5).grid(row=0, column=1)

        ttk.Label(control_frame, text="Cols A").grid(row=0, column=2)
        self.cols_a = tk.IntVar(value=2)
        ttk.Entry(control_frame, textvariable=self.cols_a, width=5).grid(row=0, column=3)

        ttk.Label(control_frame, text="Rows B").grid(row=0, column=4)
        self.rows_b = tk.IntVar(value=2)
        ttk.Entry(control_frame, textvariable=self.rows_b, width=5).grid(row=0, column=5)

        ttk.Label(control_frame, text="Cols B").grid(row=0, column=6)
        self.cols_b = tk.IntVar(value=2)
        ttk.Entry(control_frame, textvariable=self.cols_b, width=5).grid(row=0, column=7)

        ttk.Label(control_frame, text="Operation").grid(row=0, column=8)
        self.operation = ttk.Combobox(control_frame, values=["Addition", "Subtraction", "Multiplication", "Transpose A", "Determinant A", "Inverse A"])
        self.operation.grid(row=0, column=9)
        self.operation.set("Addition")

        ttk.Button(control_frame, text="Generate Matrices", command=self.generate_matrices).grid(row=0, column=10, padx=10)

        # Input fields
        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.pack(pady=10)

        # Result
        self.result_label = ttk.Label(self.root, text="Result:", font=("Segoe UI", 14, "bold"))
        self.result_label.pack(pady=5)
        self.result_box = tk.Text(self.root, height=8, width=60)
        self.result_box.pack()

    def generate_matrices(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries_a = []
        self.entries_b = []

        rows_a, cols_a = self.rows_a.get(), self.cols_a.get()
        rows_b, cols_b = self.rows_b.get(), self.cols_b.get()

        # Matrix A
        ttk.Label(self.matrix_frame, text="Matrix A").grid(row=0, column=0, columnspan=cols_a)
        for r in range(rows_a):
            row = []
            for c in range(cols_a):
                entry = ttk.Entry(self.matrix_frame, width=5)
                entry.grid(row=r+1, column=c)
                entry.insert(0, "0")
                row.append(entry)
            self.entries_a.append(row)

        # Spacer
        ttk.Label(self.matrix_frame, text="    ").grid(row=0, column=cols_a + 1)

        # Matrix B
        ttk.Label(self.matrix_frame, text="Matrix B").grid(row=0, column=cols_a + 2, columnspan=cols_b)
        for r in range(rows_b):
            row = []
            for c in range(cols_b):
                entry = ttk.Entry(self.matrix_frame, width=5)
                entry.grid(row=r+1, column=c + cols_a + 2)
                entry.insert(0, "0")
                row.append(entry)
            self.entries_b.append(row)

        ttk.Button(self.matrix_frame, text="Calculate", command=self.calculate).grid(row=max(rows_a, rows_b)+2, column=0, columnspan=10, pady=10)

    def get_matrix(self, entries):
        return np.array([[float(entry.get()) for entry in row] for row in entries])

    def calculate(self):
        try:
            A = self.get_matrix(self.entries_a)
            op = self.operation.get()
            result = ""

            if op in ["Addition", "Subtraction", "Multiplication"]:
                B = self.get_matrix(self.entries_b)

            if op == "Addition":
                result = A + B
            elif op == "Subtraction":
                result = A - B
            elif op == "Multiplication":
                result = A @ B
            elif op == "Transpose A":
                result = A.T
            elif op == "Determinant A":
                result = np.linalg.det(A)
            elif op == "Inverse A":
                result = np.linalg.inv(A)

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, (result))

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()
