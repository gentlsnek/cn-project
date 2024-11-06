import psutil
import subprocess

def get_wireless_interface():
    interfaces = psutil.net_if_addrs()
    for interface_name in interfaces:
        if 'wlan' in interface_name or 'wifi' in interface_name or 'wl' in interface_name:
            return interface_name
    return None

# Function to retrieve Wi-Fi interface details using iw
def get_iw_info():
    interface = get_wireless_interface()
    if not interface:
        print("No wireless interface found.")
        return
    try:
        result = subprocess.check_output(["iw", "dev", interface, "info"], universal_newlines=True)
        print("Wi-Fi Interface Info (via iw):")
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi interface info via iw: {e}")

# Function to retrieve signal strength and link quality using iwconfig
def get_wifi_signal_strength():
    try:
        result = subprocess.check_output(["iwconfig"], universal_newlines=True)
        print("Wi-Fi Signal Strength (via iwconfig):")
        for line in result.splitlines():
            if "Link Quality" in line:
                print(f"  {line.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi signal strength via iwconfig: {e}")

# Function to retrieve Wi-Fi info using nmcli
def get_wifi_info_nmcli():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list"], universal_newlines=True)
        print("Available Wi-Fi Networks (via nmcli):")
        for line in result.splitlines():
            ssid, signal, security = line.split(":")
            print(f"SSID: {ssid}, Signal Strength: {signal}%, Security: {security}")
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi info via nmcli: {e}")