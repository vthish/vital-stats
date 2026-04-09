import psutil
import GPUtil

def get_hardware_status():
    print("=== PC Hardware Monitor ===")
    
    # Get CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")
    
    # Get RAM Usage
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used // (1024 ** 3)
    ram_total_gb = ram.total // (1024 ** 3)
    print(f"RAM Usage: {ram.percent}% ({ram_used_gb}GB / {ram_total_gb}GB)")
    
    # Get GPU Usage and Temperature
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(f"GPU: {gpu.name}")
            print(f"GPU Load: {gpu.load * 100:.1f}%")
            print(f"GPU Temperature: {gpu.temperature}C")
    else:
        print("No GPU detected or GPUtil not supported.")
    
    print("===========================")

if __name__ == "__main__":
    get_hardware_status()