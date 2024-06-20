import TouchPortalAPI as TP
from TouchPortalAPI.logger import Logger
import sys
import os
import time
import json
import asyncio
from argparse import ArgumentParser
from TPCLIENT import TPClient
from LightController import LightController

from utils import organize_ips, get_ip_last_octet, write_lights_to_file, load_lights_from_file
from _colors import COLOR_CODES, COLOR_CODES2,  COLOR_DICT, rrggbbaa_to_rgb, get_closest_kelvin, create_empty_image_base64
from tp_entry import PLUGIN_ID, TP_PLUGIN_SETTINGS, TP_PLUGIN_ACTIONS, TP_PLUGIN_INFO, __version__, TP_PLUGIN_CONNECTORS
from pywizlight.scenes import SCENE_NAME_TO_ID
import re



PLUGIN_PATH = os.path.abspath(".\\")

#################  Fixed issue with change light brightness action
#################  Fixed issue with change light scene action
#################  Fixed issue with commands not working if ANY other light is not available but in the lights.json so I removed the need for the json file which holds previous light IP addresses&mac - not entirely sure why I implemented this previously so for now its gone.. ##



################# Setting Static IPs 
##### User should set static ip for each light, this way there is no confusion on which light belongs to which, as we are sorting the lights by IP address
### Currently we are sorting the IPs by lowest to highest 
### Secondary option may be to create a popup/config file that allows the user to set the IP address for each light and or room of lights, and then we can sort by that instead of IP address


#################  Getting Device Power Usage
## We could get power used by device, but my lights dont show any response on the test??


#### ISSUES
### If lights are not discovered properly then we need to add a way to manually add them to the list when a user tries to control it..
### 🎇 When Changing Colors, it does not reset/change the lights Icon/Image to blank, it instead remains which needs fixed.
### if changing to scene with no icon in folder, it will error.. fix this




#### Changing Light Scenes
## When Changing the light to a SCENE, the color of the icon will not change currently and the there is no icons designated for the scene name.. 
####           This will be up to the user to create/set icons for their desired scenes. 
####           Else we COULD potentially store them on base64 or local folder and change as needed.. but unsure if scenes are the same amongst many devices or not?
###            ??? make a dictionary full of the base64 images for each scene 


############## TO DO LIST
### ✅Add Kelvin Range Choice Update to Light White Action based on the lights range availability
### ✅already added to the entry.tp just need to create the function to update choicelist and to check the range of the light
### ✅Kelvin ranges kind of added, but need refined.. (perhaps just leave the base as it stands)
### ❓add option in settings where it saves lights in json to load from to maintain the same lights and their settings no matter if offline.
### ❓ Add more colors for cold white, warm white, and daylight whites (partially done, need to get Hex values for each RGB)
### have option for user to load lights, see total length of lights and then be able to resave over the config if needed..



    

g_log = Logger(name = PLUGIN_ID)

loop = asyncio.new_event_loop()

def the_async_loop():
    global loop
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run(ip_address=TP_PLUGIN_SETTINGS['Broadcast IP Address']['value']))
        return loop
    except Exception as e:
        g_log.error(e)
    finally:
       pass


def run_task(tasks):
    if not isinstance(tasks, list):
           tasks = [tasks]
    try:
        loop.run_until_complete(asyncio.gather(*[loop.create_task(task) for task in tasks]))
    except RuntimeError as e:
        if str(e) == 'This event loop is already running':
            pass  # Ignore the error if the event loop is already running
        else:
            raise  # Re-raise the error if it's a different one


def set_light_brightness( bulb_ip: str, brightness: int)-> None :
    """
    Set Light Brightness using button
    """
    ## take a 0-100 scale and convert it to 0-255
    brightness = min(int(brightness * 2.55), 255)
    try:
        run_task(controller.light_brightness(bulb_ip, brightness))
    except Exception as e:
        g_log.error("Error setting light brightness - likely adjust too fast or light is off")
    

## my attempt at an alarm.. lol
async def set_light_color_and_brightness(bulb_ip: str, color: tuple = (255, 0, 0)):
    bulb_ip = "192.168.0.156"


    brightness_levels = [50, 100, 255, 175, 50, 200]

    for brightness in brightness_levels:
        # Set the light color and brightness
        await controller.light_color(bulb_ip, color)
        await controller.light_brightness(bulb_ip, brightness)

        # Wait for 1 second before changing the brightness again
        await asyncio.sleep(0.3)

        # Turn off the light for 0.5 second
        await controller.light_off(bulb_ip)
        await asyncio.sleep(0.8)

        # Turn on the light again
        await controller.light_on(bulb_ip)


    # task = loop.create_task(set_light_color_and_brightness("asf", (255, 0, 0)))
    # loop.run_until_complete(task)



def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    if (value := settings.get(TP_PLUGIN_SETTINGS['Broadcast IP Address']['name'])) is not None:
        TP_PLUGIN_SETTINGS['Broadcast IP Address']['value'] = value
        

#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)

    ## Runs the main controller class
    the_async_loop() 





#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.info(f"Settings: {data}")
    handleSettings(data['values'])



@TPClient.on(TP.TYPES.onListChange)
def listChangeAction(data:dict):
    print(data)
    if data['actionId'] == PLUGIN_ID + ".act.light.scene_select":
        if data['listId'] == PLUGIN_ID + ".act.light.selection" and data.get('value') is not None:
           
           if data['value'] != "Custom":
            TPClient.choiceUpdate(PLUGIN_ID + ".act.light.scene_select.choice", controller.bulb_type_dict[data['value']]['supported_scenes'])
           
    if data['actionId'] == PLUGIN_ID + ".act.light.set_white":
        pass
       #if data['listId'] == PLUGIN_ID + ".act.light.set_white.type" and data.get('value') is not None:
       #    
       #    if data.get('value') == "Cold White":
       #        TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "3100", "3500", "4100"])   
       #        
       #     #   "None", "2200", "2700", "3000", "3100", "3500", "4100", "5000", "6500"
       #    if data.get('value') == "Warm White":
       #        TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "2200", "2700", "3000"])
       #    if data.get('value') == "Daylight":
       #        TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", ["None", "5000", "6500"])
       #    #TPClient.choiceUpdate(PLUGIN_ID + ".act.light.set_white.kelvin", controller.bulb_type_dict[data['value']]['kelvin_range'])

def format_lightIPs(ip_values: list) -> list:
    """ 
    Formats a list of IP addresses to ensure they are properly quoted.

    This function takes a list of IP addresses and ensures that each IP address is a string. 
    If the IP addresses are not already strings (i.e., they do not have quotes around them), 
    the function adds quotes. If the IP addresses are already strings, the function leaves them as is. 
    The function also removes any trailing commas from the list.

    Args:
        ip_values (list): A list of IP addresses, which may or may not be strings.

    Returns:
        list: A list of IP addresses, guaranteed to be strings.
    """
    
    if not ip_values.startswith('["') and not ip_values.endswith('"]'):
        ip_values = '["' + ip_values[1:-1] + '"]'

    ip_values = re.sub(",\s*\]$", "]", ip_values)
    
    if ip_values.startswith('[') and ip_values.endswith(']'):
        ip_list = json.loads(ip_values)
    else:
        raise ValueError("Invalid IP list format | IP VALUES: ", ip_values)
    
    return ip_list



#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data: dict):
    print(data)
    g_log.debug(f"Action: {data}")
    
    ### Turning on/off lights
    if data['actionId'] == PLUGIN_ID + ".act.turn.on.off.light":
        actions = {
            "On": controller.light_on,
            "Off": controller.light_off,
            "Toggle": controller.light_toggle
        }

        ip_values = data['data'][1]['value'] if data['data'][1]['value'] != "Custom" else data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([actions[data['data'][0]['value']](light_IP) for light_IP in ip_list])
    
    
    ### Light Brightness Action
    if data['actionId'] == PLUGIN_ID + ".act.light.brightness":
        brightness = int(data['data'][1]['value'])* 2.55

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_brightness(ip, brightness) for ip in ip_list])

        # TPClient.shortIdUpdate(controller.BRIGHTNESS_SHORTID, round(int(data['data'][1]['value'])/255*100))
    
    
    ### Color RGB Manual Action
    if data['actionId'] == PLUGIN_ID + ".act.light.color.rgb.manual":
        rgb_tuple = (int(data['data'][1]['value']), int(data['data'][2]['value']), int(data['data'][3]['value']))

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][4]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_color(ip, rgb_tuple) for ip in ip_list])


    ### Color RGB Action
    if data['actionId'] == PLUGIN_ID + ".act.light.color.rgb":
        rgb_tuple = rrggbbaa_to_rgb(data['data'][1]['value'].replace("#", ""))

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_color(ip, rgb_tuple) for ip in ip_list])

    
    ### Set Light White Action
    if data['actionId'] == PLUGIN_ID + ".act.light.set_white":
        brightness = int(data['data'][1]['value'])
        kelvin = int(data['data'][2]['value'])
        
        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][3]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_white(ip, brightness, kelvin) for ip in ip_list])

    
    ### Scene Select Action
    if data['actionId'] == PLUGIN_ID + ".act.light.scene_select":
        scene_id = SCENE_NAME_TO_ID[data['data'][1]['value']]

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_scene(ip, scene_id) for ip in ip_list])
    
     
    if data['actionId'] == PLUGIN_ID + ".act.discover.new_lights":
        g_log.info("Discovering new lights")
        # Discovering new lights
        controller.bulbs = asyncio.run(controller.discover_lights())
        
        ## If manually getting new lights then we will force overwrite the file with the new lights
        write_lights_to_file(controller.bulbs)
        
        # Getting bulb Type for all discovered lights
        controller.bulb_type_dict = asyncio.run(controller.get_bulb_type_bulk())
        
        ## Updating the Light/IP Choice List for Brightness Control Slider + All other Actions.
        controller.update_choices(controller.bulb_type_dict)
        
        g_log.info(f"{len(controller.bulbs)} new light(s) discovered")

    if data['actionId'] == PLUGIN_ID + ".act.light.effect_speed":
        speed = int(data['data'][1]['value'])

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.set_light_speed(light_ip = ip, speed = speed) for ip in ip_list])
        

@TPClient.on(TP.TYPES.shortConnectorIdNotification)
def on_connector_create(data:dict):
    """ Called when a connector is created """
    g_log.info(f"Connector created: {data}")
    
    if TP_PLUGIN_CONNECTORS['Brightness Control']['id'] in data['connectorId']:
        ## if no sleep here, and we do ANYTHING with settings then it throws en error?  
        time.sleep(0.5)
       # print("brightness control created")
        g_log.debug(f"Brightness ShortID: {data['shortId']}")
        controller.BRIGHTNESS_SHORTID = data['shortId']


@TPClient.on(TP.TYPES.onConnectorChange)
def onConnectorChange(data:dict):
    connector_id = data['connectorId']
    value = data['value']

    # Initialize the connector in the dictionary if it's not already there
    if connector_id not in controller.last_change:
        controller.last_change[connector_id] = {'time': 0, 'value': None}
        

    # Only proceed if it has been more than 0.1 seconds since the last change and the value has changed
    if time.time() - controller.last_change[connector_id]['time'] <= 0.105 or controller.last_change[connector_id]['value'] == value:
        return
    
    controller.last_change[connector_id] = {'time': time.time(), 'value': value}

    g_log.debug(f"Connector {connector_id} changed to {value}")

    if data['connectorId'] == PLUGIN_ID + ".connector.light.brightnessControl":
        brightness = int(data['value'])* 2.55 ## 0-255 scale

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][1]['value']
        ip_list = format_lightIPs(ip_values)
        
        run_task([controller.light_brightness(ip, brightness) for ip in ip_list])
   
        
    if data['connectorId'] == PLUGIN_ID + ".connector.light.hueControl":
        hue = str(data['value']) 

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][1]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_color(ip, COLOR_DICT[str(hue)]) for ip in ip_list])

    
    if data['connectorId'] == PLUGIN_ID + ".connector.light.whiteControl":
        kelvin = int(((6500 - 2200) * int(data['value']) / 100) + 2200) ## 2200-6500 scale

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][1]['value']
        ip_list = format_lightIPs(ip_values)

        run_task([controller.light_white(ip, 100, kelvin) for ip in ip_list])

    if data['connectorId'] == PLUGIN_ID + ".connector.light.speedControl":
        speed = int(data['value'] * 2) ## 0-200 scale

        ip_values = data['data'][0]['value'] if data['data'][0]['value'] != "Custom" else data['data'][1]['value']
        ip_list = format_lightIPs(ip_values)
     
        run_task([controller.set_light_speed(light_ip = ip, speed = speed) for ip in ip_list])


    if data['connectorId'] == PLUGIN_ID + ".connector.light.AllControl":
        ip_values = data['data'][2]['value']
        ip_list = format_lightIPs(ip_values)

        if data['data'][0]['value'].lower() == "color":
            run_task([controller.light_color(ip, COLOR_DICT[str(data['value'])]) for ip in ip_list])
            
        if data['data'][0]['value'].lower() == "brightness":
            brightness = int(data['value'])* 2.55 ## 0-255 scale
            run_task([controller.light_brightness(ip, brightness) for ip in ip_list])
    

        if data['data'][0]['value'].lower() == "white":
            kelvin = int(((6500 - 2200) * int(data['value']) / 100) + 2200) ## 2200-6500 scale

            run_task([controller.light_white(ip, 100, kelvin) for ip in ip_list])

        if data['data'][0]['value'].lower() == "speed":
            speed = int(data['value'] * 2) ## 0-200 scale

            run_task([controller.set_light_speed(light_ip = ip, speed = speed) for ip in ip_list])
    



# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data:dict):
    g_log.info('Received shutdown event from TP Client.')


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



## -- RUNNING THE CODE -- ##

async def run(ip_address: str):
    global controller
    controller = LightController(broadcast_ip=ip_address)
    await controller.main()


if __name__ == "__main__":
    sys.exit(main())





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