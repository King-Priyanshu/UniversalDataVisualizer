import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class AdvancedVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Universal Data Visualizer")
        self.root.geometry("550x320")
        self.root.configure(bg="#f4f4f4")

        self.file_path = None
        self.df = None

        # UI Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 11), padding=6)
        self.style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 12))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

        # --- GUI Widgets ---
        ttk.Label(root, text="📁 Select a data file (CSV, Excel, JSON, TXT, XML)", style="Header.TLabel").pack(pady=15)

        self.select_btn = ttk.Button(root, text="🔍 Browse File", command=self.select_file)
        self.select_btn.pack(pady=5)

        self.file_label = ttk.Label(root, text="No file selected", foreground="#555")
        self.file_label.pack(pady=5)

        self.visualize_btn = ttk.Button(root, text="📈 Visualize Data", command=self.visualize_data, state="disabled")
        self.visualize_btn.pack(pady=20)

    def select_file(self):
        filetypes = [
            ("All supported", "*.csv *.xlsx *.xls *.json *.txt *.xml"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls"),
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("XML files", "*.xml"),
        ]
        self.file_path = filedialog.askopenfilename(title="Select File", filetypes=filetypes)

        if self.file_path:
            try:
                ext = os.path.splitext(self.file_path)[1].lower()
                if ext == '.csv':
                    self.df = pd.read_csv(self.file_path)
                elif ext in ['.xlsx', '.xls']:
                    self.df = pd.read_excel(self.file_path)
                elif ext == '.json':
                    self.df = pd.read_json(self.file_path)
                elif ext == '.txt':
                    # Try comma first, fallback to tab
                    try:
                        self.df = pd.read_csv(self.file_path)
                    except:
                        self.df = pd.read_csv(self.file_path, delimiter='\t')
                elif ext == '.xml':
                    self.df = pd.read_xml(self.file_path)
                else:
                    raise ValueError("Unsupported file format!")

                self.file_label.config(text=f"✅ Loaded: {os.path.basename(self.file_path)}")
                self.visualize_btn.config(state="normal")
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")
        else:
            self.file_label.config(text="⚠️ No file selected")

    def visualize_data(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a valid file first.")
            return

        # Check necessary columns
        if 'name' not in self.df.columns or 'marks' not in self.df.columns:
            messagebox.showerror("Missing Columns", "The file must contain 'name' and 'marks' columns.")
            return

        # Visualization Window
        plot_win = tk.Toplevel(self.root)
        plot_win.title("📊 Visualizations")
        plot_win.geometry("1000x500")
        plot_win.configure(bg="#ffffff")

        fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
        fig.suptitle("Data Visualizations", fontsize=16, fontweight='bold')

        # Bar Chart
        axs[0].bar(self.df['name'], self.df['marks'], color='#4a90e2')
        axs[0].set_title("Marks by Name", fontsize=12)
        axs[0].set_xlabel("Name")
        axs[0].set_ylabel("Marks")
        axs[0].tick_params(axis='x', rotation=45)

        # Pie Chart
        axs[1].pie(self.df['marks'], labels=self.df['name'], autopct='%1.1f%%', startangle=140)
        axs[1].set_title("Marks Distribution", fontsize=12)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedVisualizer(root)
    root.mainloop()
