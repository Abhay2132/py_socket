import netifaces
import socket

def getHOST():
    """Retrieves the IP address of the active hotspot on Windows."""

    try:
        # Approach 1: Leverage netifaces for more reliable network interface identification
        gateway_iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        hotspot_addrs = netifaces.ifaddresses(gateway_iface)[netifaces.AF_INET]
        return hotspot_addrs[0]['addr']

    except KeyError:
        try:
            # Approach 2: Fallback to socket for compatibility
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)

        except Exception as e:
            print("Error retrieving IP address:", e)
            return None

HOST = getHOST()  # Standard loopback interface address (localhost)
PORT = 5002  # Port to listen on (non-privileged ports are > 1023)
