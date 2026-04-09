import psutil
import GPUtil
import customtkinter as ctk

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

def get_dynamic_color(value):
    if value < 50:
        return "#2FA572"  # Green
    elif value < 80:
        return "#E8B923"  # Yellow (Warning)
    else:
        return "#E74C3C"  # Red (Danger/High Load)

def update_stats():
    # --- CPU Update ---
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_progress.set(cpu_usage / 100) 
    cpu_progress.configure(progress_color=get_dynamic_color(cpu_usage))
    cpu_label.configure(text=f"CPU Usage: {cpu_usage}%")
    
    # --- RAM Update ---
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used // (1024 ** 3)
    ram_total_gb = ram.total // (1024 ** 3)
    ram_progress.set(ram.percent / 100)
    ram_progress.configure(progress_color=get_dynamic_color(ram.percent))
    ram_label.configure(text=f"RAM: {ram.percent}% ({ram_used_gb}GB / {ram_total_gb}GB)")
    
    # --- GPU Update ---
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_usage = gpu.load * 100
        gpu_progress.set(gpu.load)
        gpu_progress.configure(progress_color=get_dynamic_color(gpu_usage))
        
        # GPU details with line breaks (\n)
        gpu_label.configure(text=f"GPU: {gpu.name}\nLoad: {gpu_usage:.1f}%\nTemp: {gpu.temperature}°C")
    else:
        gpu_progress.set(0)
        gpu_progress.configure(progress_color="#555555")
        gpu_label.configure(text="GPU: Not detected\n\n")

    # --- Fan Speed Update (Customized for ASUS) ---
    fan_label.configure(text="Fans: Managed by System (Armoury Crate/G-Helper)", text_color="#2FA572")
    
    # Schedule the next update after 1000ms (1 second)
    root.after(1000, update_stats)

# --- GUI Setup ---
root = ctk.CTk()
root.title("Vital Stats Monitor Pro")
root.geometry("450x480")  # Height increased for multiline GPU text
root.resizable(False, False)

# Main Frame
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title Label
title_label = ctk.CTkLabel(master=frame, text="💻 Hardware Monitor Pro", font=("Roboto", 22, "bold"))
title_label.pack(pady=15)

# CPU Section
cpu_label = ctk.CTkLabel(master=frame, text="CPU Usage: --%", font=("Roboto", 14))
cpu_label.pack(pady=(5, 0))
cpu_progress = ctk.CTkProgressBar(master=frame, width=350)
cpu_progress.pack(pady=5)
cpu_progress.set(0)

# RAM Section
ram_label = ctk.CTkLabel(master=frame, text="RAM Usage: --%", font=("Roboto", 14))
ram_label.pack(pady=(10, 0))
ram_progress = ctk.CTkProgressBar(master=frame, width=350)
ram_progress.pack(pady=5)
ram_progress.set(0)

# GPU Section (justify="center" keeps the multiline text neat)
gpu_label = ctk.CTkLabel(master=frame, text="GPU: --\nLoad: --%\nTemp: --°C", font=("Roboto", 14), justify="center")
gpu_label.pack(pady=(10, 0))
gpu_progress = ctk.CTkProgressBar(master=frame, width=350)
gpu_progress.pack(pady=5)
gpu_progress.set(0)

# Fan Speed Section 
fan_label = ctk.CTkLabel(master=frame, text="Fans: Checking...", font=("Roboto", 13, "italic"), text_color="#AAAAAA")
fan_label.pack(pady=(15, 0))

# Initialize the first update
update_stats()

# Run the application
root.mainloop()