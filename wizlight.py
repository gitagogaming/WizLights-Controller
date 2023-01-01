from tp_entry import PLUGIN_ID, TP_PLUGIN_SETTINGS, TP_PLUGIN_ACTIONS, TP_PLUGIN_INFO, __version__, TP_PLUGIN_CONNECTORS
from TouchPortalAPI.logger import Logger
from argparse import ArgumentParser
import TouchPortalAPI as TP
from pprint import pprint
import sys
import os
import time
import json
from functools import wraps

from typing import Dict, Type
from typing import Callable, Dict, Optional, Tuple, cast


import asyncio
from pywizlight import wizlight, PilotBuilder, discovery, scenes
from pywizlight.models import DiscoveredBulb
from pywizlight.protocol import WizProtocol

# import logging

# def catch_errors(func):
#     def wrapper(*args, **kwargs):
#         try:
#             # Call the original function
#             return func(*args, **kwargs)
#         except Exception as e:
#             # Log the error message
#             print(f"ERROR CAUGHT IN {func.__name__}: {e}")
#             logging.exception(e)
#     return wrapper


#### This allows us to scale from 0-100 and cover the entire color spectrum
COLOR_DICT = {
    "0": (255, 0, 0),
    "1": (255, 0, 0),
    "2": (255, 16, 0),
    "3": (255, 32, 0),
    "4": (255, 48, 0),
    "5": (255, 64, 0),
    "6": (255, 80, 0),
    "7": (255, 96, 0),
    "8": (255, 112, 0),
    "9": (255, 128, 0),
    "10": (255, 144, 0),
    "11": (255, 160, 0),
    "12": (255, 176, 0),
    "13": (255, 192, 0),
    "14": (255, 208, 0),
    "15": (255, 224, 0),
    "16": (255, 240, 0),
    "17": (255, 255, 0),
    "18": (239, 255, 0),
    "19": (223, 255, 0),
    "20": (207, 255, 0),
    "21": (191, 255, 0),
    "22": (175, 255, 0),
    "23": (159, 255, 0),
    "24": (143, 255, 0),
    "25": (127, 255, 0),
    "26": (111, 255, 0),
    "27": (95, 255, 0),
    "28": (79, 255, 0),
    "29": (63, 255, 0),
    "30": (47, 255, 0),
    "31": (31, 255, 0),
    "32": (15, 255, 0),
    "33": (0, 255, 0),
    "34": (0, 255, 16),
    "35": (0, 255, 32),
    "36": (0, 255, 48),
    "37": (0, 255, 64),
    "38": (0, 255, 80),
    "39": (0, 255, 96),
    "40": (0, 255, 112),
    "41": (0, 255, 128),
    "42": (0, 255, 144),
    "43": (0, 255, 160),
    "44": (0, 255, 176),
    "45": (0, 255, 192),
    "46": (0, 255, 208),
    "47": (0, 255, 224),
    "48": (0, 255, 240),
    "49": (0, 255, 255),
    "50": (0, 239, 255),
    "51": (0, 223, 255),
    "52": (0, 207, 255),
    "53": (0, 191, 255),
    "54": (0, 175, 255),
    "55": (0, 159, 255),
    "56": (0, 143, 255),
    "57": (0, 127, 255),
    "58": (0, 111, 255),
    "59": (0, 95, 255),
    "59": (0, 95, 255),
    "60": (0, 79, 255),
    "61": (0, 63, 255),
    "62": (0, 47, 255),
    "63": (0, 31, 255),
    "64": (0, 15, 255),
    "65": (0, 0, 255),
    "66": (16, 0, 255),
    "67": (32, 0, 255),
    "68": (48, 0, 255),
    "69": (64, 0, 255),
    "70": (80, 0, 255),
    "71": (96, 0, 255),
    "72": (112, 0, 255),
    "73": (128, 0, 255),
    "74": (144, 0, 255),
    "75": (160, 0, 255),
    "76": (176, 0, 255),
    "77": (192, 0, 255),
    "78": (208, 0, 255),
    "79": (224, 0, 255),
    "80": (240, 0, 255),
    "81": (255, 0, 255),
    "82": (255, 0, 239),
    "83": (255, 0, 223),
    "84": (255, 0, 207),
    "85": (255, 0, 191),
    "86": (255, 0, 175),
    "87": (255, 0, 159),
    "88": (255, 0, 143),
    "89": (255, 0, 127),
    "90": (255, 0, 111),
    "91": (255, 0, 95),
    "92": (255, 0, 79),
    "93": (255, 0, 63),
    "94": (255, 0, 47),
    "95": (255, 0, 31),
    "96": (255, 0, 15),
    "97": (255, 0, 0),
    "98": (255, 16, 0),
    "99": (255, 32, 0),
    "100": (255, 48, 0)
}


COLOR_CODES = {
    'Cold White': {'3100': {'RGB': (255, 139, 57), 'HEX': 'ff8b39'},
                    '3500': {'RGB': (255, 182, 78), 'HEX': 'ffb64e'},
                    '4100': {'RGB': (255, 218, 122), 'HEX': 'ffda7a'}},
    'Warm White': {'2200': {'RGB': (255, 115, 23), 'HEX': 'ff7317'},
                    '2700': {'RGB': (255, 139, 39), 'HEX': 'ff8b27'},
                    '3000': {'RGB': (255, 139, 57), 'HEX': 'ff8b39'}},
    'Daylight':   {'4700': {'RGB': (255, 234, 144), 'HEX': 'ffe190'},
                    '5000': {'RGB': (255, 248, 167), 'HEX': 'fff8a7'},
                    '6500': {'RGB': (255, 249, 253), 'HEX': 'fff9fd'}}}

################## Changing Light Scenes
## When Changing the light to a SCENE, the color of the icon will not change currently and the there is no icons designated for the scene name.. 
####           This will be up to the user to create/set icons for their desired scenes. 
####           Else we COULD potentially store them on base64 or local folder and change as needed.. but unsure if scenes are the same amongst many devices or not?
###            ??? make a dictionary full of the base64 images for each scene 


################# Setting Static IPs 
##### User should set static ip for each light, this way there is no confusion on which light belongs to which, as we are sorting the lights by IP address
### Currently we are sorting the IPs by lowest to highest 
### Secondary option may be to create a popup/config file that allows the user to set the IP address for each light and or room of lights, and then we can sort by that instead of IP address

#################  Getting Device Power Usage
## We could get power used by device, but my lights dont show any response on the test??


#### ISSUES
# when lites are white and you start plugin, they return a black color.. so if the color comes back black, then we need to check if the light is white and set it to white instead of black


############## TO DO LIST
### ✅Add Kelvin Range Choice Update to Light White Action based on the lights range availability
### ✅already added to the entry.tp just need to create the function to update choicelist and to check the range of the light
### ✅Kelvin ranges kind of added, but need refined.. (perhaps just leave the base as it stands)
### ❓add option in settings where it saves lights in json to load from to maintain the same lights and their settings no matter if offline.
### ❓ Add more colors for cold white, warm white, and daylight whites (partially done, need to get Hex values for each RGB)
### If lights are not discovered properly then we need to add a way to manually add them to the list when a user tries to control it.. 
### have option for user to load lights, see total length of lights and then be able to resave over the config if needed..


loop = asyncio.new_event_loop()

try:
    TPClient = TP.Client(
        pluginId = PLUGIN_ID,  # required ID of this plugin
        sleepPeriod = 0.05,    # allow more time than default for other processes
        autoClose = True,      # automatically disconnect when TP sends "closePlugin" message
        checkPluginId = True,  # validate destination of messages sent to this plugin
        maxWorkers = 4,        # run up to 4 event handler threads
        updateStatesOnBroadcast = False,  # do not spam TP with state updates on every page change
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")

def the_async_loop():
    global loop
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run(ip_address=TP_PLUGIN_SETTINGS['Broadcast IP Address']['value']))
    except Exception as e:
        g_log.error(e)
    finally:
       pass

g_log = Logger(name = PLUGIN_ID)


def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    if (value := settings.get(TP_PLUGIN_SETTINGS['Broadcast IP Address']['name'])) is not None:
        # this example doesn't do anything useful with the setting, just saves it
        TP_PLUGIN_SETTINGS['Broadcast IP Address']['value'] = value
     #  print("\n\n\n\n")
     #  print(value)
     #  print("the ip address", TP_PLUGIN_SETTINGS['Broadcast IP Address']['value'])



#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)

    
    
    the_async_loop() 
   #loop = asyncio.get_event_loop()
   ## Run the `run` function in a separate thread or process using `run_in_executor`
   #loop.run_in_executor(None, run, ip_address="192.168.0.255")





#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
  # if (settings := data.get('values')):
  #     handleSettings(settings, False)




@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data):
    print(data)
    if data['actionId'] == PLUGIN_ID + ".act.light.scene_select":
        if data['listId'] == PLUGIN_ID + ".act.light.selection" and data.get('value') is not None:
            
           TPClient.choiceUpdate(PLUGIN_ID + ".act.light.scene_select.choice", controller.bulb_type_dict[data['value']]['supported_scenes'])
           
    if data['actionId'] == PLUGIN_ID + ".act.light.set_white":
        if data['listId'] == PLUGIN_ID + ".act.light.set_white.type" and data.get('value') is not None:
           # print(data['data'][4]['value'])
            #print("The Kelvin range", controller.bulb_type_dict[data['data'][4]['value']]['kelvin_range'])
            if data.get('value') == "Cold White":
                TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "3100", "3500", "4100"])
            if data.get('value') == "Warm White":
                TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "2200", "2700", "3000"])
            if data.get('value') == "Daylight":
                TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "5000", "6500"])
            #TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", controller.bulb_type_dict[data['value']]['kelvin_range'])




#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    print(data)
    g_log.debug(f"Action: {data}")
    
    ### Turning on/off lights
    if data['actionId'] == PLUGIN_ID + ".act.turn.on.off.light":
        ## Checking to see if custom light wanted
        if data['data'][1]['value'] == "Custom":
            the_ip = data['data'][2]['value']
        else:
            the_ip = data['data'][1]['value']
        
        if data['data'][0]['value'] == "On":  
            task = loop.create_task(controller.light_on(the_ip))
            loop.run_until_complete(task)
        elif data['data'][0]['value'] == "Off":
            task = loop.create_task(controller.light_off(the_ip))
            loop.run_until_complete(task)
        elif data['data'][0]['value'] == "Toggle":
            task = loop.create_task(controller.light_toggle(the_ip))
            loop.run_until_complete(task)
    
    
    ### Light Brightness Action
    if data['actionId'] == PLUGIN_ID + ".act.light.brightness":
        if data['data'][1]['value'] == "Custom":
            the_ip = data['data'][2]['value']
        else:
            the_ip = data['data'][1]['value']
            
        set_light_brightness(the_ip, int(data['data'][1]['value']))
        TPClient.shortIdUpdate(controller.BRIGHTNESS_SHORTID, round(int(data['data'][1]['value'])/255*100))
    
    ### Color RGB Manual Action
    if data['actionId'] == PLUGIN_ID + ".act.light.color.rgb.manual":
        if data['data'][0]['value'] == "Custom":
            the_ip = data['data'][4]['value']
        else:
            the_ip = data['data'][0]['value']
            
        # Creating a tuple from data1, data2, data3
        rgb_tuple = (int(data['data'][1]['value']), int(data['data'][2]['value']), int(data['data'][3]['value']))
        task = loop.create_task(controller.light_color(the_ip, rgb_tuple))
        loop.run_until_complete(task)
    
    ### Color RGB Action
    if data['actionId'] == PLUGIN_ID + ".act.light.color.rgb":
        if data['data'][0]['value'] == "Custom":
            the_ip = data['data'][2]['value']
        else:
            the_ip = data['data'][0]['value']
            
        ## Convert the RRGGBBAA  value to a RGB tuple
        rgb_tuple = rrggbbaa_to_rgb(data['data'][1]['value'].replace("#", ""))
        task = loop.create_task(controller.light_color(the_ip, rgb_tuple))
        loop.run_until_complete(task)
    
    
    ### Set Light White Action
    if data['actionId'] == PLUGIN_ID + ".act.light.set_white":
        if data['data'][0]['value'] == "Custom":
            the_ip = data['data'][4]['value']
        else:
            the_ip = data['data'][0]['value']
        
        kelvin = int(data['data'][3]['value'])
        task = loop.create_task(controller.light_white(the_ip, data['data'][1]['value'], int(data['data'][2]['value']), kelvin))
        loop.run_until_complete(task)
    
    
    ### Scene Select Action
    if data['actionId'] == PLUGIN_ID + ".act.light.scene_select":
        """ 
        This is able to Set the Scene Color for the selected light OR a list of lights
        """
        thelist = None
        
        if data['data'][0]['value'] == "Custom":
            the_ip = data['data'][2]['value']
            
            ## else if data['data'][0]['value'] contains 'LIST' then load it as a list
            if data['data'][2]['value'].startswith('['):
                thelist  = json.loads(data['data'][2]['value'])
        else:
            ## else we just use the normal IP
            the_ip = data['data'][0]['value']
            
        if thelist:
            for ip in thelist:
                #   find the index of the scene in the list of supported scenes starting with 1 instead of 0
                index = controller.bulb_type_dict[ip]['supported_scenes'].index(data['data'][1]['value'])
                index = index +1
                task = loop.create_task(controller.light_scene(ip, int(index)))
                loop.run_until_complete(task)
        
        else:
            index = controller.bulb_type_dict[the_ip]['supported_scenes'].index(data['data'][1]['value'])
            index = index +1
            task = loop.create_task(controller.light_scene(the_ip, int(index)))
            loop.run_until_complete(task)
        
         
         
    if data['actionId'] == PLUGIN_ID + ".act.discover.new_lights":
        g_log.info("Discovering new lights")
        
        # Discovering new lights
        task = loop.create_task(controller.discover_lights())
        loop.run_until_complete(task)
        controller.bulbs = task.result()
        
        
        ## If manually getting new lights then we will force overwrite the file with the new lights
        controller.write_lights_to_file(controller.bulbs)
        
        # Getting bulb Type for all discovered lights
        task = loop.create_task(controller.get_bulb_type_bulk())
        loop.run_until_complete(task)
        controller.bulb_type_dict = task.result()
        
        ## Updating the Light/IP Choice List for Brightness Control Slider + All other Actions.
        controller.update_choices(controller.bulb_type_dict)
        
        g_log.info(f"{len(controller.bulbs)} new light(s) discovered")



def set_light_brightness(bulb_ip: str, brightness: int):
    """
    Set Light Brightness using Slider 
    """
    ## take a 0-100 scale and convert it to 0-255
    brightness = min(int(brightness * 2.55), 255)
    task = loop.create_task(controller.light_brightness(bulb_ip, brightness))
  # if loop.is_running():
  #     pass
  # else:
    loop.run_until_complete(task)
    





@TPClient.on(TP.TYPES.shortConnectorIdNotification)
def on_connector_create(data):
    """ Called when a connector is created """
    g_log.info(f"Connector created: {data}")
    
    if TP_PLUGIN_CONNECTORS['Brightness Control']['id'] in data['connectorId']:
        ## if no sleep here, and we do ANYTHING with settings then it throws en error?  
        time.sleep(0.5)
       # print("brightness control created")
        g_log.debug(f"Brightness ShortID: {data['shortId']}")
        controller.BRIGHTNESS_SHORTID = data['shortId']


#import colorsys

#def rgb_to_hex(rgb):
#    # Round the values in the RGB tuple to integers
#    rgb = tuple(map(int, rgb))
#    return '#%02x%02x%02x' % rgb


# def scale_to_hex_color(scale):
#     # Calculate the hue value as the scale value divided by 100, and multiplied by 360
#     hue = scale / 100 * 360
#     # Convert the hue value to an RGB tuple with fixed lightness and saturation values
#     rgb = colorsys.hls_to_rgb(hue / 360, 0.5, 0.5)
#     # Round the values of the RGB tuple to the nearest integer
#     rgb = tuple(round(x) for x in rgb)
#     return rgb
# 


@TPClient.on(TP.TYPES.onConnectorChange)
def connectors(data):
  #  print(data)
    if data['connectorId'] == PLUGIN_ID + ".connector.light.brightnessControl":
        
        
        if data['data'][0]['value']:
            if data['data'][0]['value'] == "Custom":
                set_light_brightness(data['data'][1]['value'], int(data['value']))
                ## TP States get set in the set_light_brightness function
                
            elif data['data'][0]['value'] != "Custom":
                set_light_brightness(bulb_ip=data['data'][0]['value'], brightness=int(data['value']))
        
        
        
    if data['connectorId'] == PLUGIN_ID + ".connector.light.hueControl":
        if data['data'][0]['value']:
            ip = data['data'][0]['value']
            if data['data'][0]['value'] == "Custom":
                ip = data['data'][1]['value']
                
            ## Scaling the Color Wheel Based on Slider Value
            task = loop.create_task(controller.light_color(ip, COLOR_DICT[str(data['value'])]))
            loop.run_until_complete(task)



# from PIL import Image

#def create_color_scale_image(color_scale):
#    # Determine the dimensions of the image
#    width = 100
#    height = 20
#    # Create an image with the desired dimensions
#    img = Image.new("RGB", (width, height))
#    # Extract the colors from the dictionary and put them in a list
#    colors = [color for key, color in color_scale.items()]### 
#    ## put these colors on each row of the image
#    img.putdata(colors)
#    return img
#
#img = create_color_scale_image(COLOR_DICT)
#img.show()


# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')
    # We do not need to disconnect manually because we used `autoClose = True`











class LightController:
    def __init__(self, broadcast_ip: str):
        self.broadcast_ip = broadcast_ip
        self.bulbs = []
        self.bulb_type_dict = {}
        self.BRIGHTNESS_SHORTID = ""
        
        
    async def main(self):
        """ 
        Discover all bulbs in the network via Broadcast datagram (UDP)
        - function takes the discovery object and returns a list of wizlight objects.
        """
        self.bulbs = await self.discover_lights()
        self.bulb_type_dict = await self.get_bulb_type_bulk()
        
        
    def thecallback(self):
        """
        Callback function for the state change.
        - DOES NOT WORK YET....
        """
        g_log.info(f"State changed: ")
    



    async def discover_lights(self) -> list:
        """
        Discovers lights in the network and compares them to the previously discovered lights. If there are any new lights, they are added to the list and saved to a file.
        
        Returns:
            A list of wizlight objects.
        """
        # Load the previously discovered lights from the file
        loaded_lights = self.load_lights_from_file()
        
        # If the lights were loaded from the file, compare them to the currently discovered lights
        if loaded_lights:
            g_log.info("The Lights were loaded.. we dont need to discover?")
            
            self.bulbs = loaded_lights
            
            ## save self.bulbs to text file
            self.write_lights_to_file(loaded_lights, "lights.txt")
        
            return self.bulbs
            
        # If the lights were not loaded from the file, discover the lights and save them to the file
        else:
            g_log.info("The Lights were NOT loaded.. we need to discover?")
            self.bulbs = await discovery.discover_lights(broadcast_space=self.broadcast_ip, wait_time=1)
            self.write_lights_to_file(self.bulbs)
        return self.bulbs



    async def get_bulb_type_bulk(self) -> dict:
        """
        Get the bulb type.
        """
        bulb_type_dict = {}
        
        ## Sorting the list of lights by IP address
        sorted_wizlight_list = sorted(self.bulbs, key=self.get_ip_last_octet)
        
        
        for index, bulb in enumerate(sorted_wizlight_list):
            
            ip_octet = self.get_ip_last_octet(bulb)
            
            supported_scenes = await bulb.getSupportedScenes()
            bulb_type = await bulb.get_bulbtype()
            
            ##### Some lights might not accept brightness/color/color_tmp/effect
            #### We should perhaps update action data based on this information but this would combine most light actions into one which may not be very user friendly
            light_color_rgb = await self.get_light_color(bulb.ip)
            
            light = wizlight(bulb.ip)
            ## create a dictionary with the data below 
            bulb_type_dict.update({bulb.ip: {'features':
                                                {
                                                'brightness': bulb_type.features.brightness,
                                                'color': bulb_type.features.color, 
                                                'color_tmp': bulb_type.features.color_tmp,
                                                'effect': bulb_type.features.effect},
                                                'kelvin_range': {'max': bulb_type.kelvin_range.max, 
                                                                'min': bulb_type.kelvin_range.min}, 
                                                'name': bulb_type.name,
                                                "supported_scenes": supported_scenes,
                                                "current_color": str(light_color_rgb),
                                                "TheLight": light,  ### We could store each light in a dictionary and then reference that later and not have to remake the light object all the time??
                                                                    ### but then anything using this as self.bulb_type_dict[light_ip]['TheLight'] works fine, but it doesnt highlight properly in vS code to know its an actual function/working object
                                                }
                                           })
            
            ## Creating a state for each light
            TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", description="WIZ | Light Icon/Color: " + str(ip_octet), value="", parentGroup=str("Light " + str(ip_octet)))
            ## set bulb.ip as state
            TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".ip", description="WIZ | Light IP: " + str(ip_octet), value=str(bulb.ip), parentGroup=str("Light " + str(ip_octet)))
            
            # Creating a state for each light             
           # light = wizlight(bulb.ip)               # Setting Light object
            light_state = await light.updateState() # Getting Light States
            light_status = light_state.get_state()  # Getting Current Light Status
            
            ## Checking if Light has a scene, if not set to none
            light_scene = light_state.get_scene() # Getting Current Light Scene
            if light_scene:
                TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", description="WIZ | Light Scene: " + str(ip_octet), value=light_scene, parentGroup=str("Light " + str(ip_octet)))
                g_log.info(f"Light {ip_octet} - {bulb.ip} Scene: {light_scene}")
                
            if not light_scene:
                TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", description="WIZ | Light Scene: " + str(ip_octet), value="None", parentGroup=str("Light " + str(ip_octet)))
                g_log.info(f"Light {ip_octet} - {bulb.ip} Scene: 'None'")
                
            brightness = str(light_state.get_brightness()) # Getting Current Light Brightness
           # print("this is the brightness: ", type(brightness))
            if brightness != "None":
                new_brightness = (int(brightness) / 255) * 100
                TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", description="WIZ | Light Brightness: " + str(ip_octet), value=str(round(new_brightness)), parentGroup=str("Light " + str(ip_octet)))
            
            
            # ## Adding Effect State if supported by light
            # if bulb_type.features.effect:
            #     TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".effect", description="WIZ | Light Effect" + str(ip_octet), value=light_state., parentGroup=str("Light " + str(ip_octet)))
            
            if bulb_type.features.color_tmp:   ## Adding Color Temp State if supported by light
                TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", description="WIZ | Light Color Temp: " + str(ip_octet), value=str(light_state.get_colortemp()) , parentGroup=str("Light " + str(ip_octet)))
            
            
            # State Creation for Light Status
            TPClient.createState(f"{PLUGIN_ID}.state.light.{str(ip_octet)}.status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
            
            #  ## State Create for Light Brightness
            #  TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", description="WIZ | Light Brightness" + str(ip_octet), value=light_state.__dict__['pilotResult'].get('dimming', ""), parentGroup=str("Light " + str(ip_octet)))
            
            
            if light_color_rgb[1] != None:
                ahex = '%02x%02x%02x' % light_color_rgb  ## Taking an RGB value and turning into Hex - Setting Icon Color for Light
                aarrggbb = f'#FF{ahex}'
               
                 ## updating the icon color state
                 #   TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", description="WIZ | Light Icon/Color" + str(ip_octet), value="", parentGroup=str("Light " + str(ip_octet)))
                if aarrggbb == "#FF000000":
                    ## if its black then we setting it as white cause theres no way its black? 
                    if light_state.get_cold_white() != "0":
                        aarrggbb = "#FF" + COLOR_CODES['Cold White']['HEX']
                    if light_state.get_warm_white() == "0":
                        aarrggbb = "#FF" + COLOR_CODES['Warm White']['HEX']
                        
                    TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", stateValue=aarrggbb)
                
                
        # # Updating the List of Light Choices for the Actions, This would be the Lights IP Address as thats our best form of identification other than mac address
        self.update_choices(bulb_type_dict)
        
        return bulb_type_dict





    
    def update_light_state(func):
        """ My first decorartor. It updates the light status after a light action is performed. """
        @wraps(func)
        async def wrapper(self, light_ip: str):
            
            print("this is the light ip: ", light_ip)
            try:
                light = wizlight(light_ip)
                result = await func(self, light)

                light_state = await light.updateState()
                light_status = light_state.get_state()

                ip_octet = controller.get_ip_last_octet(light)
               # TPClient.stateUpdate(f"{PLUGIN_ID}.state.light.{str(ip_octet)}.status", stateValue=str(light_status))
                TPClient.createState(f"{PLUGIN_ID}.state.light.{str(ip_octet)}.status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
                brightness = str(light_state.get_brightness()) # Getting Current Light Brightness
                # print("this is the brightness: ", type(brightness))
                if brightness != "None":
                    ### Creating the state here because if its not found in list and user has CUSTOM Light set up then it wouldnt be created by default, so now it should make all states as expected.
                    
                #    new_brightness = (int(brightness) / 255) * 100
                    TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", description="WIZ | Light Brightness: " + str(ip_octet), value=str(light_state.__dict__['pilotResult']['dimming']), parentGroup=str("Light " + str(ip_octet)))
                    ## one for color temp
                    TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", description="WIZ | Light Color Temp: " + str(ip_octet), value=str(light_state.get_colortemp()) , parentGroup=str("Light " + str(ip_octet)))
                    ## and for status
                    TPClient.createState(f"{PLUGIN_ID}.state.light.{str(ip_octet)}.status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
                    
                    ## and for scene - IT WONT WORK FOR SCENE? SCene is a string.. heck its force to a string.. why is it not working?
                    TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", description="WIZ | Light Scene: " + str(ip_octet), value=str(light_state.get_scene()), parentGroup=str("Light " + str(ip_octet)))

                g_log.info(f"{light_ip} - Light Status: {light_status}")
                return result
            except Exception as e:
                print("this is the error: ", e)
        return wrapper
    
    
    @update_light_state
    async def light_on(self, light: wizlight):
        await light.turn_on()
        
    @update_light_state
    async def light_off(self, light: wizlight):
        await light.turn_off()
        
    @update_light_state
    async def light_toggle(self, light: wizlight):
        await light.lightSwitch()
    
    
    
    async def light_white(self, light_ip:str, lighttype:str, brightness:int, kelvin:int = 2700):
        """
        Turn on a white light at the specified IP address with the given brightness and color temperature (in kelvins).
        Parameters:
        - light_ip: The IP address of the light to turn on.
        - lighttype: The type of white light to turn on. Can be "Warm White", "Cold White", or "Daylight".
        - brightness: The brightness of the light, from 0 to 255.
        - kelvin: The color temperature of the light, in kelvins. Default is 2700K.
        
        Returns:
        None
        """
        # Create a wizlight object for the light at the given IP address
        light = wizlight(light_ip)
        
        # If the brightness is greater than 255, set it to 255
        if brightness > 255:
            brightness = 255
        
        # Set the warm_white and cold_white values depending on the lighttype
        if lighttype == "Warm White":
            warm_white = brightness
            cold_white = 0
        elif lighttype == "Cold White":
            warm_white = 0
            cold_white = brightness
        elif lighttype == "Daylight":
            warm_white = 0
            cold_white = brightness
        
        # Turn on the light with the specified warm_white, cold_white, brightness, and color temperature values
        await light.turn_on(PilotBuilder(warm_white=warm_white, cold_white=cold_white, brightness=int(brightness * 2.55), colortemp=kelvin))
        
        # Change the color of the light's icon to the appropriate RGB value from the COLOR_CODES dictionary
        self.change_light_icon_color(light_ip, COLOR_CODES[lighttype][str(kelvin)]['RGB'])
        
        # Get the index of the light and set its "scene" to "None" using the TPClient.stateUpdate method
        #index = self.get_light_index(light_ip)
        
        ip_octet = self.get_ip_last_octet(light)
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue="None")
    
    

    
    async def light_brightness(self, light_ip: str, brightness: int):
        """
        Change the brightness of a light.

        Parameters:
            light_ip (str): IP address of the light.
            brightness (int): Brightness level of the light, from 0 to 255.

        Notes:
            - The `light_ip` parameter should correspond to a valid light IP in the `bulb_type_dict` dictionary.
            - The `brightness` parameter should be an integer value between 0 and 255.
            - If the `brightness` parameter is less than or equal to 255, the light will be turned on with the specified brightness level.
            - The `PLUGIN_ID` constant and `ip_octet` variable should be defined elsewhere in the code.
            - Need to find a way to show an actual object when referencing the dictionary object
        """
        theLight = self.bulb_type_dict[light_ip]['TheLight']
        ip_octet = controller.get_ip_last_octet(self.bulb_type_dict[light_ip]['TheLight'])
        if brightness <= 255:
            await theLight.turn_on(PilotBuilder(brightness=brightness))
            new_brightness = (int(brightness) / 255) * 100
            TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) + ".brightness", str(round(new_brightness)))


    
    
    async def light_color(self, light_ip:str, color: tuple):
        """
        Change the color of a light at the specified IP address and update the light's icon color in Touch Portal.
        
        Parameters:
        - light_ip: The IP address of the light to change the color of.
        - color: A tuple containing the RGB values for the desired color, in the range 0-255.
        
        Returns:
        None
        """
        # If a light_ip was specified, change the color of the light
        if light_ip:
            # Create a wizlight object for the light at the given IP address
            light = wizlight(light_ip)
            
            # Turn on the light with the specified color
            await light.turn_on(PilotBuilder(rgb = color))
            
            # Update the bulb_type_dict with the current color of the light
            self.bulb_type_dict[light_ip]['current_color'] = color
            
            # Change the color of the light's icon to the specified color
            cur_color = self.change_light_icon_color(light_ip, color)
            
            # Get the last 3 octet of the light and set its "scene" to "None" using the TPClient.stateUpdate method
            ip_octet = self.get_ip_last_octet(light)
            TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue="None")
            
            # Log the current color of the light
            g_log.info(f"{light_ip} | Current Color: "+ cur_color)
    
    
     
    async def light_scene(self, light_ip:str, scene_id:int):
        """
        Change the scene of a light at the specified IP address and update the scene in Touch Portal.
    
        Parameters:
        - light_ip: The IP address of the light to change the scene of.
        - scene_id: The ID of the scene to set.
    
        Returns:
        None
        """
        # Create a wizlight object for the light at the given IP address
        light = wizlight(light_ip)
    
        # Turn on the light with the specified scene
        await light.turn_on(PilotBuilder(scene =scene_id))
    
        # Update the state of the light and get the name of the current scene
        state = await light.updateState()
        g_log.info(f"{light_ip} | Current Scene: "+ state.get_scene())
    
        # Get the index of the light and set its "scene" to the current scene using the TPClient.stateUpdate method
       # index = controller.get_light_index(light_ip)
        ip_octet = self.get_ip_last_octet(light)
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue=state.get_scene())
    
    
    
    
    async def light_effect(self, light_ip: str, speed: int):
        """
        Set the speed of a light's effect.
        
        Parameters:
            light_ip (str): IP address of the light.
            speed (int): Speed of the light's effect, from 10 to 200.
            
        Notes:
            - The `speed` parameter should be an integer value between 10 and 200.
            - If the `speed` parameter is less than 10, it will be set to 10.
            - If the `speed` parameter is greater than 200, it will be set to 200.
        """
        light = wizlight(light_ip)
        set_speed = max(10, min(speed, 200))
        await light.set_speed(set_speed)
        ip_octet = self.get_ip_last_octet(light)
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) + ".effect_speed", stateValue=str(set_speed))

    
    
    
    async def get_light_color(self, light_ip:str):
        """
        Get the current color of a light at the specified IP address.
        Parameters:
        - light_ip: The IP address of the light to get the color of.
        
        Returns:
        A tuple containing the RGB values of the light's current color, in the range 0-255.
        """
        
        # Create a wizlight object for the light at the given IP address
        light = wizlight(light_ip)
        # Update the state of the light and get the RGB values
        state = await light.updateState()
        red, green, blue = state.get_rgb()
        
        # Return the RGB values as a tuple
        return (red, green, blue)
    
    
    
    
    def change_light_icon_color(self, light_ip:str, color: tuple):
        """ 
        This function changes the icon color for the light set at that Index
        How can we get names set in the app to show up here instead of going by Light Index?  
        """
        
        ### convert rgb tuple to hex
        try:
            ahex = '%02x%02x%02x' % color
        except TypeError:
            color = tuple(map(int, color))
            ahex = '%02x%02x%02x' % color
            
        aarrggbb = f'#FF{ahex}'
   
        ip_octet = self.get_ip_last_octet(self.bulb_type_dict[light_ip]['TheLight'])
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", stateValue=aarrggbb)
        return aarrggbb





################################### UTIL STYLE THINGS

    def load_lights_from_file(self) -> list:
        """
        Loads a list of wizlight objects from a JSON file.
        
        Returns:
            A list of wizlight objects. If the file does not exist or there is an error
            reading the file, an empty list is returned.
        """
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



    def write_lights_to_file(self, wizlight_list, file_name='wizlight_list.json'):
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



    def get_ip_last_octet(self, wizlight):
        """ 
        Making sure the list of lights is sorted by IP address and the last 3 octets
        """
        octets = wizlight.ip.split(".")
        return int(octets[3])

    # def create_annotated_dict(data: Dict[str, Dict[str, Type[wizlight]]]):
    #     return data

    def get_light_index(self, light_ip:str):
        """ 
        This function gets the index of the light in the bulb_type_dict
        """
        index = list(controller.bulb_type_dict.keys()).index(light_ip)
        return index


    def organize_ips(self, ip_addresses):
        """
        Organizes the List of IP addressed based on the last two or three octets
        """
        def sort_key(ip_octets):
            return '.'.join(ip_octets[-2:])
        
        sorted_ips = sorted(list(map(lambda x: x.split('.'), ip_addresses)), key=sort_key)
        return list(map(lambda x: '.'.join(x), sorted_ips))
    
    
    
    
    
    def update_choices(self, bulb_type_dict):
        """ 
        This function updates the choices for the light selection. 
        """
        IP_LIST = self.organize_ips(list(bulb_type_dict.keys()))
        IP_LIST.append("Custom")
        TPClient.choiceUpdate(PLUGIN_ID + ".act.light.selection",
                              values=list(IP_LIST))
        TPClient.choiceUpdate(PLUGIN_ID + ".connector.light.brightnessControl.choices",
                              values=list(IP_LIST))








## main
def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    # default log file destination
    logFile = f"./{PLUGIN_ID}.log"
    # default log stream destination
    logStream = sys.stdout
    
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")

    # his processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting {TP_PLUGIN_INFO['name']} v{__version__} on {sys.platform}.")

    try:
        TPClient.connect()
    #   loop = asyncio.get_event_loop()
    #   loop.run_until_complete(run(ip_address="192.168.0.255"))

        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret













## --------------------- UTILS --------------------------- ##

def rrggbbaa_to_rgb(color):
    """ 
    Convert a color string from the format "rrggbbaa" to a tuple of integers
    """
    # Extract the red, green, and blue values from the color string
    red = color[0:2]
    green = color[2:4]
    blue = color[4:6]
    
    # Convert the red, green, and blue values from hexadecimal to decimal
    red = int(red, 16)
    green = int(green, 16)
    blue = int(blue, 16)
    # Return the converted values as a tuple
    return (red, green, blue)







## -- RUNNING THE CODE -- ##

# To use the class, you can instantiate an object and call the main method
async def run(ip_address: str):
    global controller
    controller = LightController(broadcast_ip=ip_address)
    await controller.main()

# Don't forget to use `asyncio.run` if you're running this code in a
# script (outside of a function that is already marked as async)
#asyncio.run(main(ip_address="192.168.0.255"))

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main(ip_address="192.168.0.255"))




if __name__ == "__main__":
    sys.exit(main())






























   #The old way - async def light_white(self, light_ip:str, lighttype:str, brightness:int, kelvin:int = 2700):
   #The old way -     kelv_str = str(kelvin)
   #The old way -     light = wizlight(light_ip)
   #The old way -     if brightness > 256:
   #The old way -             brightness = 255
   #The old way -     
   #The old way -     
   #The old way -     
   #The old way -     if lighttype == "Warm White":
   #The old way -         ## warm_white takes a value from 0-255 but it does nothing??
   #The old way -         await light.turn_on(PilotBuilder(warm_white=int(brightness), brightness = int(brightness * 2.55), colortemp=kelvin))
   #The old way -        # self.change_light_icon_color(light_ip, COLOR_CODES['Warm White']['RGB']) ## Setting Icon to a warm white color
   #The old way -         self.change_light_icon_color(light_ip, COLOR_CODES[lighttype][kelv_str]['RGB']) 
   #The old way -        # COLOR_CODES['Warm White']['RGB']
   #The old way -     elif lighttype == "Cold White":
   #The old way -         ## cold_white takes a value from 0-255 but it does nothing??
   #The old way -         ## making sure to never send more than 100 
   #The old way -         await light.turn_on(PilotBuilder(cold_white=int(brightness), brightness = int(brightness * 2.55), colortemp=kelvin))
   #The old way -         #self.change_light_icon_color(light_ip, COLOR_CODES['Cold White']['RGB'])    ## Setting Icon to a Cool white color
   #The old way -         self.change_light_icon_color(light_ip, COLOR_CODES[lighttype][kelv_str]['RGB']) 
   #The old way -         
   #The old way -     elif lighttype == "Daylight":
   #The old way -         await light.turn_on(PilotBuilder(cold_white=brightness,brightness=int(brightness * 2.55), colortemp=kelvin))
   #The old way -       #  self.change_light_icon_color(light_ip, COLOR_CODES['Cold White']['RGB']) 
   #The old way -         self.change_light_icon_color(light_ip, COLOR_CODES[lighttype][kelv_str]['RGB']) 
   #The old way -         
   #The old way -     
   #The old way -     ## if we set color then we should change the 'scene of the light to none'
   #The old way -     index = controller.get_light_index(light_ip)
   #The old way -     TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(index) +".scene", stateValue="None")
        
        
        
        



















    
    
    # Set up a standard light
  #temp rem -  light = wizlight("192.168.0.138")
  #temp rem -  # Set up the light with a custom port
  #temp rem -  #light = wizlight("your bulb's IP address", port=12345)

  #temp rem -  # The following calls need to be done inside an asyncio coroutine
  #temp rem -  # to run them from normal synchronous code, you can wrap them with
  #temp rem -  # asyncio.run(..).

  #temp rem -  # Turn the light on into "rhythm mode"
  #temp rem -  await light.turn_on(PilotBuilder())
  #temp rem -  # Set bulb brightness
  #temp rem -  await light.turn_on(PilotBuilder(brightness = 255))

  #temp rem -  # Set bulb brightness (with async timeout)
  #temp rem -  timeout = 10
  #temp rem -  await asyncio.wait_for(light.turn_on(PilotBuilder(brightness = 255)), timeout)

  #temp rem -  # Set bulb to warm white
  #temp rem -  await light.turn_on(PilotBuilder(warm_white = 255))

  #temp rem -  # Set RGB values
  #temp rem -  # red to 0 = 0%, green to 128 = 50%, blue to 255 = 100%
  #temp rem -  await light.turn_on(PilotBuilder(rgb = (0, 128, 255)))

  #temp rem -  # Get the current color temperature, RGB values
  #temp rem -  state = await light.updateState()
  #temp rem -  print(state.get_colortemp())
  #temp rem -  red, green, blue = state.get_rgb()
  #temp rem -  print(f"red {red}, green {green}, blue {blue}")

  #temp rem -  # Start a scene
  #temp rem -  await light.turn_on(PilotBuilder(scene = 4)) # party

  #temp rem -  # Get the name of the current scene
  #temp rem -  state = await light.updateState()
  #temp rem -  print(state.get_scene())




    # Get the features of the bulb
 # bulb_type = await bulbs[0].get_bulbtype()
 # print(bulb_type.features.brightness) # returns True if brightness is supported
 # print(bulb_type.features.color) # returns True if color is supported
 # print(bulb_type.features.color_tmp) # returns True if color temperatures are supported
 # print(bulb_type.features.effect) # returns True if effects are supported
 # print(bulb_type.kelvin_range.max) # returns max kelvin in INT
 # print(bulb_type.kelvin_range.min) # returns min kelvin in INT
 # print(bulb_type.name) # returns the module name of the bulb

    # Turn the light off
 #   await light.turn_off()

    # Do operations on multiple lights in parallel
    #bulb1 = wizlight("<your bulb1 ip>")
    #bulb2 = wizlight("<your bulb2 ip>")
    # --- DEPRECATED in 3.10 see [#140](https://github.com/sbidy/pywizlight/issues/140)
    # await asyncio.gather(bulb1.turn_on(PilotBuilder(brightness = 255)),
    #    bulb2.turn_on(PilotBuilder(warm_white = 255)))
    # --- For >3.10 await asyncio.gather() from another coroutine
    # async def turn_bulbs_on(bulb1, bulb2):
    #    await asyncio.gather(bulb1.turn_on(PilotBuilder(warm_white=255)), bulb2.turn_on(PilotBuilder(warm_white=255)))
    #  def main:
    #    asyncio.run(async turn_bulbs_on(bulb1, bulb2))

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())



#import asyncio
#from pywizlight import wizlight, PilotBuilder
#
#import asyncio
#from pywizlight import wizlight, PilotBuilder
#
#async def looping_gradient_light(ip_address: str):
#    # Set up the light
#    light = wizlight(ip_address)
#    
#    # Turn the light on
#    await light.turn_on(PilotBuilder())
#    await light.turn_on(PilotBuilder(brightness = 200))
#   # g=0
#    while True:
#        # Create the gradient effect from red to green
#        # Set the light to a solid red
#     #   print(g)
#     #   await light.turn_on(PilotBuilder(rgb = (255, g, 0)))
#      #  await asyncio.sleep(1)
#        
#        # Gradually change the color to green
#        for i in range(256):
#            # Set the RGB values to a gradient between red and green
#            r = 255 - (i * 255 / 256)
#            g = i * 255 / 256
#            b = 0
#         #   print(int(r))
#            await light.turn_on(PilotBuilder(rgb = (int(r), int(g), int(b))))
#            # Wait for 10 milliseconds before changing the color again
#            await asyncio.sleep(0.01)
#        
#        # Create the gradient effect from green to red
#        for i in range(256):
#          #  print(r)
#            # Set the RGB values to a gradient between green and red
#            r = i * 255 / 256
#            g = 255 - (i * 255 / 256)
#            b = 0
#            await light.turn_on(PilotBuilder(rgb = (int(r), int(g), int(b))))
#            # Wait for 10 milliseconds before changing the color again
#            await asyncio.sleep(0.01)
#    
#  #  # Turn the light off
#  #  await light.turn_off()
#    
#async def main():
#    await looping_gradient_light("192.168.0.138")
#
#asyncio.run(main())
#
#
#
#def reformat_message(message, chatbadge_count, username):
#    lines = message.split('<newline>')
#    result = ""
#    for i in range(0, len(lines)):
#        line = lines[i]
#        # Subtract 3 spaces for each chat badge
#        line_length = 49 - (3 * chatbadge_count)
#        # For the first line, subtract the length of the username and a colon and a space
#        if i == 0:
#            line_length -= len(username)
#        # Add the necessary number of spaces to align the text to the right
#        line = line + '⠀' * (line_length - len(line))
#        if i > 0:
#          result += '\n' + line
#        else:
#          result += line
#        print("------")
#        print("THE RESULT", result)
#        print("------")
#
#
#
#    with open('test.txt', 'w', encoding='utf-8') as f:
#        f.write(result)
#    return result
  
  

    
#reformat_message("Testing again wewt<newline>Does it work<newline> As expected???<newline>", 2, "GitagoGaming")