import customtkinter as ctk
import psutil
import GPUtil
import socket
import platform
from datetime import datetime
import threading
from PIL import Image
import pystray

# =========================
# APP CONFIG
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WIDTH = 1400
HEIGHT = 850

# =========================
# COLORS
# =========================
BG = "#0B0F19"
CARD = "#121826"

BLUE = "#00BFFF"
GREEN = "#00FF99"
PURPLE = "#B026FF"
YELLOW = "#FFC300"
RED = "#FF4C4C"

TEXT = "#FFFFFF"
TEXT2 = "#9CA3AF"

# =========================
# WINDOW
# =========================
root = ctk.CTk()
root.title("VitalStats X")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(fg_color=BG)

# =========================
# FUNCTIONS
# =========================
def dynamic_color(value):
    if value < 50:
        return GREEN
    elif value < 80:
        return YELLOW
    return RED


def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for _, entries in temps.items():
                for entry in entries:
                    return f"{entry.current}°C"
    except:
        pass

    return "N/A"


def create_card(parent, title, color):
    frame = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=25,
        border_width=1,
        border_color=color
    )

    title_label = ctk.CTkLabel(
        frame,
        text=title,
        font=("Segoe UI", 24, "bold"),
        text_color=color
    )

    title_label.pack(anchor="w", padx=20, pady=(20, 5))

    return frame


def update_dashboard():

    # ================= CPU =================
    cpu = psutil.cpu_percent()

    cpu_bar.set(cpu / 100)
    cpu_bar.configure(progress_color=dynamic_color(cpu))

    cpu_value.configure(text=f"{cpu}%")

    cpu_temp.configure(
        text=f"Temperature : {get_cpu_temp()}"
    )

    # ================= RAM =================
    ram = psutil.virtual_memory()

    ram_bar.set(ram.percent / 100)
    ram_bar.configure(progress_color=dynamic_color(ram.percent))

    ram_value.configure(text=f"{ram.percent}%")

    ram_info.configure(
        text=f"{ram.used // (1024**3)} GB / {ram.total // (1024**3)} GB"
    )

    # ================= GPU =================
    gpus = GPUtil.getGPUs()

    if gpus:
        gpu = gpus[0]

        gpu_load = gpu.load * 100

        gpu_bar.set(gpu.load)
        gpu_bar.configure(progress_color=dynamic_color(gpu_load))

        gpu_value.configure(text=f"{gpu_load:.1f}%")

        gpu_info.configure(
            text=f"{gpu.name} | {gpu.temperature}°C"
        )

    else:
        gpu_value.configure(text="N/A")
        gpu_info.configure(text="No GPU Found")

    # ================= DISK =================
    disk = psutil.disk_usage('/')

    disk_bar.set(disk.percent / 100)
    disk_bar.configure(progress_color=dynamic_color(disk.percent))

    disk_value.configure(text=f"{disk.percent}%")

    disk_info.configure(
        text=f"{disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB"
    )

    # ================= NETWORK =================
    net = psutil.net_io_counters()

    upload_label.configure(
        text=f"Upload : {round(net.bytes_sent / (1024**2), 1)} MB"
    )

    download_label.configure(
        text=f"Download : {round(net.bytes_recv / (1024**2), 1)} MB"
    )

    # ================= CLOCK =================
    current_time = datetime.now().strftime("%I:%M:%S %p")
    time_label.configure(text=current_time)

    root.after(1000, update_dashboard)


# =========================
# SYSTEM TRAY
# =========================
def quit_window(icon, item):
    icon.stop()
    root.destroy()


def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def hide_window():
    root.withdraw()

    image = Image.new('RGB', (64, 64), color=(20, 20, 20))

    menu = (
        pystray.MenuItem('Open', show_window),
        pystray.MenuItem('Exit', quit_window)
    )

    icon = pystray.Icon(
        "VitalStats X",
        image,
        "VitalStats X",
        menu
    )

    icon.run()


def minimize_to_tray():
    threading.Thread(target=hide_window, daemon=True).start()


# =========================
# HEADER
# =========================
header = ctk.CTkFrame(root, fg_color="#0A0F1A", height=70)
header.pack(fill="x")

logo = ctk.CTkLabel(
    header,
    text="⚡ VITALSTATS X",
    font=("Segoe UI", 32, "bold"),
    text_color=BLUE
)

logo.pack(side="left", padx=20, pady=15)

time_label = ctk.CTkLabel(
    header,
    text="--:--:--",
    font=("Segoe UI", 22),
    text_color=TEXT
)

time_label.pack(side="right", padx=20)

# =========================
# BODY
# =========================
body = ctk.CTkFrame(root, fg_color="transparent")
body.pack(fill="both", expand=True, padx=20, pady=20)

body.grid_columnconfigure((0, 1), weight=1)
body.grid_rowconfigure((0, 1), weight=1)

# =========================
# CPU CARD
# =========================
cpu_card = create_card(body, "CPU", BLUE)
cpu_card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

cpu_value = ctk.CTkLabel(
    cpu_card,
    text="0%",
    font=("Segoe UI", 54, "bold")
)

cpu_value.pack(anchor="w", padx=20)

cpu_bar = ctk.CTkProgressBar(cpu_card, width=500, height=20)
cpu_bar.pack(padx=20, pady=20)

cpu_temp = ctk.CTkLabel(
    cpu_card,
    text="Temperature",
    font=("Segoe UI", 16),
    text_color=TEXT2
)

cpu_temp.pack(anchor="w", padx=20)

# =========================
# RAM CARD
# =========================
ram_card = create_card(body, "RAM", PURPLE)
ram_card.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

ram_value = ctk.CTkLabel(
    ram_card,
    text="0%",
    font=("Segoe UI", 54, "bold")
)

ram_value.pack(anchor="w", padx=20)

ram_bar = ctk.CTkProgressBar(ram_card, width=500, height=20)
ram_bar.pack(padx=20, pady=20)

ram_info = ctk.CTkLabel(
    ram_card,
    text="RAM INFO",
    font=("Segoe UI", 16),
    text_color=TEXT2
)

ram_info.pack(anchor="w", padx=20)

# =========================
# GPU CARD
# =========================
gpu_card = create_card(body, "GPU", GREEN)
gpu_card.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

gpu_value = ctk.CTkLabel(
    gpu_card,
    text="0%",
    font=("Segoe UI", 54, "bold")
)

gpu_value.pack(anchor="w", padx=20)

gpu_bar = ctk.CTkProgressBar(gpu_card, width=500, height=20)
gpu_bar.pack(padx=20, pady=20)

gpu_info = ctk.CTkLabel(
    gpu_card,
    text="GPU INFO",
    font=("Segoe UI", 16),
    text_color=TEXT2
)

gpu_info.pack(anchor="w", padx=20)

# =========================
# SYSTEM CARD
# =========================
system_card = create_card(body, "SYSTEM", YELLOW)
system_card.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

system_name = ctk.CTkLabel(
    system_card,
    text=f"{platform.system()} {platform.release()}",
    font=("Segoe UI", 18)
)

system_name.pack(anchor="w", padx=20, pady=(10, 5))

pc_name = ctk.CTkLabel(
    system_card,
    text=socket.gethostname(),
    font=("Segoe UI", 18)
)

pc_name.pack(anchor="w", padx=20)

disk_value = ctk.CTkLabel(
    system_card,
    text="0%",
    font=("Segoe UI", 36, "bold")
)

disk_value.pack(anchor="w", padx=20, pady=(20, 0))

disk_bar = ctk.CTkProgressBar(system_card, width=500, height=18)
disk_bar.pack(padx=20, pady=10)

disk_info = ctk.CTkLabel(
    system_card,
    text="DISK INFO",
    font=("Segoe UI", 16),
    text_color=TEXT2
)

disk_info.pack(anchor="w", padx=20)

upload_label = ctk.CTkLabel(
    system_card,
    text="Upload",
    font=("Segoe UI", 15)
)

upload_label.pack(anchor="w", padx=20, pady=(20, 0))

download_label = ctk.CTkLabel(
    system_card,
    text="Download",
    font=("Segoe UI", 15)
)

download_label.pack(anchor="w", padx=20)

# =========================
# FOOTER BUTTONS
# =========================
footer = ctk.CTkFrame(root, fg_color="transparent")
footer.pack(fill="x", pady=(0, 20))

tray_btn = ctk.CTkButton(
    footer,
    text="Minimize To Tray",
    width=220,
    height=45,
    corner_radius=12,
    command=minimize_to_tray
)

tray_btn.pack(side="left", padx=20)

exit_btn = ctk.CTkButton(
    footer,
    text="Exit",
    fg_color=RED,
    hover_color="#B22222",
    width=140,
    height=45,
    corner_radius=12,
    command=root.destroy
)

exit_btn.pack(side="right", padx=20)

# =========================
# START
# =========================
update_dashboard()

root.mainloop()