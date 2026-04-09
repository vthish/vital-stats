import psutil
import GPUtil
import tkinter as tk
from tkinter import ttk

def update_stats():
    # Update CPU Usage
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    
    # Update RAM Usage
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used // (1024 ** 3)
    ram_total_gb = ram.total // (1024 ** 3)
    ram_label.config(text=f"RAM Usage: {ram.percent}% ({ram_used_gb}GB / {ram_total_gb}GB)")
    
    # Update GPU Usage and Temperature
    gpus = GPUtil.getGPUs()
    if gpus:
        # Assuming the primary GPU (like the RTX 3050) is at index 0
        gpu = gpus[0]
        gpu_info = f"GPU: {gpu.name}\nLoad: {gpu.load * 100:.1f}%\nTemp: {gpu.temperature}°C"
        gpu_label.config(text=gpu_info)
    else:
        gpu_label.config(text="GPU: Not detected")
    
    # Schedule the update_stats function to run again after 1000ms (1 second)
    root.after(1000, update_stats)

# --- GUI Setup ---
root = tk.Tk()
root.title("Vital Stats Monitor")
root.geometry("350x250")
root.resizable(False, False)

# Main Frame for padding
frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# Title Label
title_label = ttk.Label(frame, text="💻 PC Hardware Monitor", font=("Arial", 14, "bold"))
title_label.pack(pady=(0, 15))

# Stats Labels
cpu_label = ttk.Label(frame, text="CPU Usage: --%", font=("Arial", 12))
cpu_label.pack(pady=5)

ram_label = ttk.Label(frame, text="RAM Usage: --%", font=("Arial", 12))
ram_label.pack(pady=5)

gpu_label = ttk.Label(frame, text="GPU: --", font=("Arial", 12), justify=tk.CENTER)
gpu_label.pack(pady=10)

# Initialize the first update
update_stats()

# Start the application
root.mainloop()