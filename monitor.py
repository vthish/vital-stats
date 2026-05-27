import psutil
import GPUtil
import customtkinter as ctk
from datetime import datetime
import platform
import socket

# =========================
# APP CONFIG
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_WIDTH = 820
APP_HEIGHT = 520

# =========================
# MAIN WINDOW
# =========================
root = ctk.CTk()
root.title("VitalStats X")
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.resizable(False, False)

# =========================
# COLORS
# =========================
BG_CARD = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
TEXT_SECONDARY = "#B5B5B5"

GREEN = "#2ECC71"
YELLOW = "#F1C40F"
RED = "#E74C3C"
BLUE = "#3B82F6"

# =========================
# FUNCTIONS
# =========================
def get_dynamic_color(value):
    if value < 50:
        return GREEN
    elif value < 80:
        return YELLOW
    return RED


def format_bytes(size):
    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]

    while size > power:
        size /= power
        n += 1

    return f"{size:.2f} {units[n]}"


def update_dashboard():

    # ================= CPU =================
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_freq = psutil.cpu_freq()

    cpu_bar.set(cpu_usage / 100)
    cpu_bar.configure(progress_color=get_dynamic_color(cpu_usage))

    cpu_label.configure(
        text=f"{cpu_usage}%"
    )

    cpu_info.configure(
        text=f"Frequency : {cpu_freq.current:.0f} MHz"
    )

    # ================= RAM =================
    ram = psutil.virtual_memory()

    ram_bar.set(ram.percent / 100)
    ram_bar.configure(progress_color=get_dynamic_color(ram.percent))

    ram_label.configure(
        text=f"{ram.percent}%"
    )

    ram_info.configure(
        text=f"{ram.used // (1024**3)} GB / {ram.total // (1024**3)} GB"
    )

    # ================= DISK =================
    disk = psutil.disk_usage('/')

    disk_bar.set(disk.percent / 100)
    disk_bar.configure(progress_color=get_dynamic_color(disk.percent))

    disk_label.configure(
        text=f"{disk.percent}%"
    )

    disk_info.configure(
        text=f"{disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB"
    )

    # ================= NETWORK =================
    net = psutil.net_io_counters()

    upload_speed.configure(
        text=f"Upload : {format_bytes(net.bytes_sent)}"
    )

    download_speed.configure(
        text=f"Download : {format_bytes(net.bytes_recv)}"
    )

    # ================= GPU =================
    gpus = GPUtil.getGPUs()

    if gpus:
        gpu = gpus[0]

        gpu_usage = gpu.load * 100

        gpu_bar.set(gpu.load)
        gpu_bar.configure(progress_color=get_dynamic_color(gpu_usage))

        gpu_label.configure(
            text=f"{gpu_usage:.1f}%"
        )

        gpu_info.configure(
            text=f"{gpu.name} | {gpu.temperature}°C"
        )

    else:
        gpu_bar.set(0)
        gpu_bar.configure(progress_color="#555555")

        gpu_label.configure(text="N/A")
        gpu_info.configure(text="GPU Not Detected")

    # ================= TIME =================
    now = datetime.now().strftime("%I:%M:%S %p")
    time_label.configure(text=now)

    # ================= SYSTEM =================
    os_label.configure(
        text=f"{platform.system()} {platform.release()}"
    )

    pc_label.configure(
        text=socket.gethostname()
    )

    root.after(1000, update_dashboard)


# =========================
# HEADER
# =========================
header = ctk.CTkFrame(root, height=70, fg_color="#111111")
header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="⚡ VitalStats X",
    font=("Segoe UI", 28, "bold")
)
title.pack(side="left", padx=20, pady=15)

time_label = ctk.CTkLabel(
    header,
    text="--:--:--",
    font=("Segoe UI", 18)
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
cpu_card = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=20)
cpu_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(
    cpu_card,
    text="CPU",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=20, pady=(20, 5))

cpu_label = ctk.CTkLabel(
    cpu_card,
    text="0%",
    font=("Segoe UI", 38, "bold")
)
cpu_label.pack(anchor="w", padx=20)

cpu_bar = ctk.CTkProgressBar(cpu_card, width=320, height=20)
cpu_bar.pack(padx=20, pady=15)
cpu_bar.set(0)

cpu_info = ctk.CTkLabel(
    cpu_card,
    text="Frequency",
    text_color=TEXT_SECONDARY
)
cpu_info.pack(anchor="w", padx=20)

# =========================
# RAM CARD
# =========================
ram_card = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=20)
ram_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(
    ram_card,
    text="Memory",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=20, pady=(20, 5))

ram_label = ctk.CTkLabel(
    ram_card,
    text="0%",
    font=("Segoe UI", 38, "bold")
)
ram_label.pack(anchor="w", padx=20)

ram_bar = ctk.CTkProgressBar(ram_card, width=320, height=20)
ram_bar.pack(padx=20, pady=15)
ram_bar.set(0)

ram_info = ctk.CTkLabel(
    ram_card,
    text="RAM Details",
    text_color=TEXT_SECONDARY
)
ram_info.pack(anchor="w", padx=20)

# =========================
# GPU CARD
# =========================
gpu_card = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=20)
gpu_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(
    gpu_card,
    text="GPU",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=20, pady=(20, 5))

gpu_label = ctk.CTkLabel(
    gpu_card,
    text="0%",
    font=("Segoe UI", 38, "bold")
)
gpu_label.pack(anchor="w", padx=20)

gpu_bar = ctk.CTkProgressBar(gpu_card, width=320, height=20)
gpu_bar.pack(padx=20, pady=15)
gpu_bar.set(0)

gpu_info = ctk.CTkLabel(
    gpu_card,
    text="GPU Details",
    text_color=TEXT_SECONDARY
)
gpu_info.pack(anchor="w", padx=20)

# =========================
# SYSTEM CARD
# =========================
system_card = ctk.CTkFrame(body, fg_color=BG_CARD, corner_radius=20)
system_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

ctk.CTkLabel(
    system_card,
    text="System",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=20, pady=(20, 10))

os_label = ctk.CTkLabel(
    system_card,
    text="OS",
    font=("Segoe UI", 18)
)
os_label.pack(anchor="w", padx=20, pady=5)

pc_label = ctk.CTkLabel(
    system_card,
    text="PC",
    font=("Segoe UI", 18)
)
pc_label.pack(anchor="w", padx=20, pady=5)

# DISK
disk_label_title = ctk.CTkLabel(
    system_card,
    text="Disk Usage",
    font=("Segoe UI", 16, "bold")
)
disk_label_title.pack(anchor="w", padx=20, pady=(15, 5))

disk_label = ctk.CTkLabel(
    system_card,
    text="0%",
    font=("Segoe UI", 22, "bold")
)
disk_label.pack(anchor="w", padx=20)

disk_bar = ctk.CTkProgressBar(system_card, width=320, height=16)
disk_bar.pack(padx=20, pady=8)
disk_bar.set(0)

disk_info = ctk.CTkLabel(
    system_card,
    text="Disk Info",
    text_color=TEXT_SECONDARY
)
disk_info.pack(anchor="w", padx=20)

# NETWORK
upload_speed = ctk.CTkLabel(
    system_card,
    text="Upload : 0 MB",
    font=("Segoe UI", 15)
)
upload_speed.pack(anchor="w", padx=20, pady=(15, 0))

download_speed = ctk.CTkLabel(
    system_card,
    text="Download : 0 MB",
    font=("Segoe UI", 15)
)
download_speed.pack(anchor="w", padx=20)

# =========================
# START
# =========================
update_dashboard()

root.mainloop()