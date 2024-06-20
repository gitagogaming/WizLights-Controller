## Util 
from TouchPortalAPI.logger import Logger
from tp_entry import PLUGIN_ID, TP_PLUGIN_SETTINGS, TP_PLUGIN_ACTIONS, TP_PLUGIN_INFO, __version__, TP_PLUGIN_CONNECTORS
import json
import os

from pywizlight import wizlight, PilotBuilder, discovery, scenes
from pywizlight.models import DiscoveredBulb
from pywizlight.protocol import WizProtocol

g_log = Logger(name = PLUGIN_ID)

def get_ip_last_octet(wizlight, onstart=False):
    """ 
    Making sure the list of lights is sorted by IP address and the last 3 octets
    """
    if onstart:
        octets = wizlight.split(".")
        return int(octets[3])
    
    octets = wizlight.ip.split(".")
    return int(octets[3])


def organize_ips(ip_addresses):
    """
    Organizes the List of IP addressed based on the last two or three octets
    """
    def sort_key(ip_octets):
        return '.'.join(ip_octets[-2:])
    
    sorted_ips = sorted(list(map(lambda x: x.split('.'), ip_addresses)), key=sort_key)
    return list(map(lambda x: '.'.join(x), sorted_ips))









def load_lights_from_file() -> list:
    """
    Loads a list of wizlight objects from a JSON file.
    
    Returns:
        A list of wizlight objects. If the file does not exist or there is an error
        reading the file, an empty list is returned.
    """
    print("loading lights from file")
    # Load the JSON file
    light_file = "wizlight_list.json"
    if os.path.exists(light_file):
        try:
            with open(light_file, 'r') as infile:
                json_data = json.load(infile)
        except Exception as e:
            g_log.error("Error loading JSON file: " + str(e))
            return []
        
        # Create a list of wizlight objects from the JSON data
        wizlight_list = []
        for wizlight_data in json_data:
            wizlight_list.append(wizlight(ip=wizlight_data['ip'], port=wizlight_data['port'], mac=wizlight_data['mac']))
            
        g_log.info("Returning the list of lights from the file")
        return wizlight_list
    else:
        return []





def write_lights_to_file(wizlight_list, file_name='wizlight_list.json'):
        """
        Writes a list of wizlight objects to a JSON file.
        Args:
            wizlight_list: A list of wizlight objects to be written to the file.
            
        Returns:
            True if the write was successful, False otherwise.
        """
        # Define a key function to extract the last 3 octets of the ip as an integer
        def get_ip_key(wizlight):
            ip_octets = wizlight.ip.split('.')[-3:]
            return int(''.join(ip_octets))
        
        # Sort the list of wizlight objects by the last 3 octets of the ip
        sorted_wizlight_list = sorted(wizlight_list, key=get_ip_key)
        
        # Convert the list of wizlight objects to a list of dictionaries
        json_data = []
        for wizlight in sorted_wizlight_list:
            json_data.append({
                'ip': wizlight.ip,
                'port': wizlight.port,
                'mac': wizlight.mac
            })
            
        g_log.info("Writing the list of lights to the file")
        # Save the JSON-formatted data to a file
        try:
            with open(file_name, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            return True
        except Exception as e:
            g_log.error("Error writing to JSON file: " + str(e))
            return False
        

# import socket
# import ipaddress

# def get_broadcast_address():
#     # Create a socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     # Connect to a remote server
#     s.connect(("8.8.8.8", 80))

#     # Get the local IP address
#     local_ip = s.getsockname()[0]

#     # Calculate the broadcast address
#     ip_interface = ipaddress.ip_interface(f"{local_ip}/24")
#     broadcast_address = ip_interface.network.broadcast_address

#     return str(broadcast_address)
