from utils import organize_ips, get_ip_last_octet, write_lights_to_file
from _colors import COLOR_CODES, get_closest_kelvin
from tp_entry import PLUGIN_ID, __version__, TP_PLUGIN_CONNECTORS
from TouchPortalAPI import tools
from TouchPortalAPI.logger import Logger
import time
import os
from functools import wraps

from pywizlight import wizlight, PilotBuilder, discovery, PilotParser
from pywizlight.scenes import SCENE_NAME_TO_ID
from _colors import COLOR_CODES, COLOR_CODES2,  COLOR_DICT, rrggbbaa_to_rgb, get_closest_kelvin, create_empty_image_base64

from TPCLIENT import TPClient

PLUGIN_PATH = os.path.abspath(".\\")
import threading    
import asyncio


## the color_temp and other details not updting on startup..
## color/hue not changing in state updates? if we have it.. icon_color
## same thing for scene.. scene needs to show 'something' when we start right? if no scene.. should it be None or just blank ???

g_log = Logger(name = PLUGIN_ID)
class LightController:
    # instance = None
    def __init__(self, broadcast_ip: str):
        self.loop = asyncio.new_event_loop()
        self.broadcast_ip = broadcast_ip
        self.bulbs = []
        self.bulb_type_dict = {}
        self.BRIGHTNESS_SHORTID = ""


        self.last_change = {}
        
    # @staticmethod
    # def the_async_loop(ip_address):
    #     loop = asyncio.new_event_loop()
    #     try:
    #         asyncio.set_event_loop(loop)
    #         LightController.instance = LightController(ip_address)
    #         loop.run_until_complete(LightController.instance.run())
    #     except Exception as e:
    #         g_log.error(e)
    #     finally:
    #         pass

    # async def run(self):
    #     await self.main()
        
    async def main(self):
        """ 
        Discover all bulbs in the network via Broadcast datagram (UDP)
        - function takes the discovery object and returns a list of wizlight objects.
        """
        self.bulbs = await self.discover_lights()
        self.bulb_type_dict = await self.get_bulb_type_bulk()
        


    def thecallback(self, state:PilotParser):

        ## does not trigger if we change stuff in the wizlight app or other places...  
        ## Not sure what the point of this is when you can get the bulb state when you update it..
        # Print the new state of the bulb
        print(f'State changed: {state.pilotResult}')



    async def discover_lights(self) -> list:
        """
        Discovers lights in the network and compares them to the previously discovered lights. If there are any new lights, they are added to the list and saved to a file.
        
        Returns:
            A list of wizlight objects.
        """
        # Load the previously discovered lights from the file
        # loaded_lights = load_lights_from_file()
        
        # # If the lights were loaded from the file, compare them to the currently discovered lights
        # if loaded_lights:
        #     g_log.info("The Lights were loaded.. we dont need to discover?")
            
        #     self.bulbs = loaded_lights
            
        # # ## save self.bulbs to text file
        # # write_lights_to_file(loaded_lights, "lights.txt")
        
        #     return self.bulbs
            
        # If the lights were not loaded from the file, discover the lights and save them to the file
        # else:
        g_log.info("The Lights were NOT loaded.. we need to discover?")
        if self.broadcast_ip == "":
            self.bulbs = await discovery.discover_lights(wait_time=1)
        else:
            self.bulbs = await discovery.discover_lights(broadcast_space=self.broadcast_ip, wait_time=1)
        write_lights_to_file(self.bulbs)
        return self.bulbs


    def set_light_scene_icon(self, ip_octet, light_scene):
        """
        Set the icon for a light's scene.
        
        Parameters:
            ip_octet (int): The last octet of the light's IP address.
            light_scene (str): The name of the light scene.
            
        Notes:
            - The `PLUGIN_PATH` and `PLUGIN_ID` constants should be defined elsewhere in the code.
        """
        
       # theimage = create_empty_image_base64()
        try:
            theimage = tools.Tools.convertImage_to_base64(PLUGIN_PATH + rf'\Icons_WizLight\{light_scene}.png')
        except:
            print("Setting the image to none")
            theimage = tools.Tools.convertImage_to_base64(PLUGIN_PATH + rf'\Icons_WizLight\none.png')
        time.sleep(0.5)
        ## make a state to update it
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) + ".icon_image", theimage)

        # async def get_bulb_type_bulk(self) -> dict:
        # """
        # Get the bulb type.
        # """
        # g_log.info("Getting Bulb Type for all discovered lights")
        # bulb_type_dict = {}
        
        # # Sorting the list of lights by IP address
        # sorted_wizlight_list = sorted(self.bulbs, key=get_ip_last_octet)
        
        # for index, bulb in enumerate(sorted_wizlight_list):
        #     ip_octet = get_ip_last_octet(bulb)
    
        #     g_log.info(f"Getting Bulb Type for Light {ip_octet}")
        #     supported_scenes = await bulb.getSupportedScenes()
        #     bulb_type = await bulb.get_bulbtype()
            
        #     light = wizlight(bulb.ip)
        #     light_color_rgb = await self.get_light_color(light)
            
        #     # create a dictionary with the data below 
        #     bulb_type_dict.update({bulb.ip: {
        #         'features': {
        #             'brightness': bulb_type.features.brightness,
        #             'color': bulb_type.features.color, 
        #             'color_tmp': bulb_type.features.color_tmp,
        #             'effect': bulb_type.features.effect
        #         },
        #         'kelvin_range': {
        #             'max': bulb_type.kelvin_range.max, 
        #             'min': bulb_type.kelvin_range.min
        #         }, 
        #         'name': bulb_type.name,
        #         "supported_scenes": supported_scenes,
        #         "current_color": str(light_color_rgb),
        #         "TheLight": light,
        #         "current_scene": None  
        #     }})
            
        #     # Creating a various Light states for the lights
        #     thestates = ["brightness", "color_temp", "scene", "kelvin", "icon_color", "icon_image"]
        #     for x in thestates:
        #         g_log.debug("Creating State: " + str(x) + " for light: " + str(ip_octet))
        #         TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +f".{x}", description=f"WIZ | {x.capitalize()}: "+ str(ip_octet), value="", parentGroup=str("Light " + str(ip_octet)))
            
        #     # Getting Light States
        #     light_state = await light.updateState()
        #     # Getting Current Light Status
        #     light_status = light_state.get_state()
        #     # Getting Current Light Scene
        #     light_scene = light_state.get_scene()
            
        #     bulb_type_dict[bulb.ip]['current_scene'] = light_scene
    
        #     # Update the states at the end
        #     TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".ip", description="WIZ | Light IP: " + str(ip_octet), value=str(bulb.ip), parentGroup=str("Light " + str(ip_octet)))
        #     TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
            
        #     if light_scene:
        #         TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue=light_scene)
        #         if light_scene in ['Daylight', 'Warm White', 'Cool White', 'Night Light']:
        #             color_temp = light_state.get_colortemp() # Getting Current Light Color Temp
        #             if color_temp:
        #                 kelvin_color = get_closest_kelvin(color_temp)
        #                 self.change_light_icon_color(bulb.ip, kelvin_color, True)
        #                 self.set_light_scene_icon(ip_octet, light_scene)
        #         else:
        #             self.set_light_scene_icon(ip_octet, light_scene)
            
        #     if light_scene == None:
        #         self.set_light_scene_icon(ip_octet, str(light_scene))
        #         if light_color_rgb[0] == None:
        #             color_temp = light_state.get_colortemp() # Getting Current Light Color Temp
        #             TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", stateValue=str(color_temp))
        #             kelvin_color = get_closest_kelvin(color_temp)
        #             self.change_light_icon_color(bulb.ip, kelvin_color, True)
        #         else:
        #             self.change_light_icon_color(bulb.ip, light_color_rgb, True)
            
        #     brightness = str(light_state.get_brightness()) # Getting Current Light Brightness
        #     if brightness != "None":
        #         new_brightness = (int(brightness) / 255) * 100
        #         TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", stateValue=str(round(new_brightness)))
            
        #     if light_color_rgb[1] != None:
        #         ahex = '%02x%02x%02x' % light_color_rgb  # Taking an RGB value and turning into Hex - Setting Icon Color for Light
        #         aarrggbb = f'#FF{ahex}'
        #         if aarrggbb == "#FF000000":
        #             if light_state.get_cold_white() != "0":
        #                 aarrggbb = "#FF" + COLOR_CODES['Cold White']['HEX']
        #             if light_state.get_warm_white() == "0":
        #                 aarrggbb = "#FF" + COLOR_CODES['Warm White']['HEX']
        #         TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", stateValue=aarrggbb)
        
        # self.update_choices(bulb_type_dict)
        
        # return bulb_type_dict      
        
    async def get_bulb_type_bulk(self) -> dict:
        """
        Get the bulb type.
        """
        g_log.info("Getting Bulb Type for all discovered lights")
        bulb_type_dict = {}
        
        ## Sorting the list of lights by IP address
        sorted_wizlight_list = sorted(self.bulbs, key=get_ip_last_octet)
        
        
        for index, bulb in enumerate(sorted_wizlight_list):
            
            await bulb.start_push(self.thecallback) ## attempting to get callback data on the bulb.. but it doesnt work yet
            
            ip_octet = get_ip_last_octet(bulb)

            g_log.info(f"Getting Bulb Type for Light {ip_octet}")
            supported_scenes = await bulb.getSupportedScenes()
            
            bulb_type = await bulb.get_bulbtype()
            
            ##### Some lights might not accept brightness/color/color_tmp/effect
            #### We should perhaps update action data based on this information but this would combine most light actions into one which may not be very user friendly
            
            light = wizlight(bulb.ip)
            light_color_rgb = await self.get_light_color(light)
            ## create a dictionary with the data below 
            bulb_type_dict.update({bulb.ip: {'features':
                                                {
                                                'brightness': bulb_type.features.brightness,
                                                'color': bulb_type.features.color, 
                                                'color_tmp': bulb_type.features.color_tmp,
                                                'effect': bulb_type.features.effect
                                                },
                                            'kelvin_range': {'max': bulb_type.kelvin_range.max, 
                                                            'min': bulb_type.kelvin_range.min}, 
                                            'name': bulb_type.name,
                                            "supported_scenes": supported_scenes,
                                            "current_color": str(light_color_rgb),
                                            "TheLight": light,  ### We could store each light in a dictionary and then reference that later and not have to remake the light object all the time??
                                                                    ### but then anything using this as self.bulb_type_dict[light_ip]['TheLight'] works fine, but it doesnt highlight properly in vS code to know its an actual function/working object
                                            "current_scene": None  
                                                }
                                           })
            
            # print("The bulb type dict", bulb_type_dict)
            ### Creating a various Light states for the lights
            thestates = ["brightness", "color_temp", "scene", "kelvin", "icon_color", "icon_image"]
            for x in thestates:
                g_log.debug("Creating State: " + str(x) + " for light: " + str(ip_octet))
                TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +f".{x}", description=f"WIZ | {x.capitalize()}: "+ str(ip_octet), value="", parentGroup=str("Light " + str(ip_octet)))
         

            # Creating a state for each light             
            light_state = await light.updateState() # Getting Light States
            light_status = light_state.get_state()  # Getting Current Light Status
            

            
            ## Create IP State
            TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".ip", description="WIZ | Light IP: " + str(ip_octet), value=str(bulb.ip), parentGroup=str("Light " + str(ip_octet)))
            
            ## Creating the lights status
            TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".status", description="WIZ | Light Status: " + str(ip_octet), value="", parentGroup=str("Light " + str(ip_octet)))
            TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
            
            ## Checking if Light has a scene, if not set to none
            light_scene = light_state.get_scene() # Getting Current Light Scene

            bulb_type_dict[bulb.ip]['current_scene'] = light_scene



            
            if light_scene:
                ## update the scene if it exists
                TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue=light_scene)
               # TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", description="WIZ | Light Scene: " + str(ip_octet), value=light_scene, parentGroup=str("Light " + str(ip_octet)))
               
                ## If its a white color scene then lets get the color temp and change icon color as expected
                if light_scene in ['Daylight', 'Warm White', 'Cool White', 'Night Light']:
                    color_temp = light_state.get_colortemp() # Getting Current Light Color Temp
                    if color_temp:
                        ## Setting the Icon to the hex color of the color temp
                        kelvin_color = get_closest_kelvin(color_temp)
                        self.change_light_icon_color(bulb.ip, kelvin_color, True)
                        g_log.debug("This is color_temp {} for {}".format(color_temp, ip_octet))
                     #   theimage = tools.Tools.convertImage_to_base64(PLUGIN_PATH + rf'\Icons_WizLight\blank.png')
                        self.set_light_scene_icon(ip_octet, light_scene)
                else:
                    ## Setting the Lights Scene Icon If possible
                    self.set_light_scene_icon(ip_octet, light_scene)
                    
                    
                g_log.info(f"Light {ip_octet} - {bulb.ip} Scene: {light_scene}")
            
            if light_scene == None:

                #threading.Thread(target=self.set_light_scene_icon, kwargs={'ip_octet': ip_octet, 'light_scene': str(light_scene)}).start()
                self.set_light_scene_icon(ip_octet, str(light_scene))  ## If there is no scene, then set scene to "none" which is a name of blank.png image
                
                if light_color_rgb[0] == None:
                    color_temp = light_state.get_colortemp() # Getting Current Light Color Temp
                    TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", stateValue=str(color_temp))
                    
                    ## If Light_Color_RGB Tuple comes back with none, then we color it based on Color_Temp
                    kelvin_color = get_closest_kelvin(color_temp)
                    self.change_light_icon_color(bulb.ip, kelvin_color, True)
                else:
                    TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", stateValue="None")
                    ## else there is a color we use the original Tuple
                    self.change_light_icon_color(bulb.ip, light_color_rgb, True)
            
            brightness = str(light_state.get_brightness()) # Getting Current Light Brightness
            if brightness != "None":
                new_brightness = (int(brightness) / 255) * 100
                ## update brightness state
                TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", stateValue=str(round(new_brightness)))
            
            
            if light_color_rgb[1] != None:
                ahex = '%02x%02x%02x' % light_color_rgb  ## Taking an RGB value and turning into Hex - Setting Icon Color for Light
                aarrggbb = f'#FF{ahex}'
               
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
        """Decorator that updates the light status after a light action is performed."""
        @wraps(func)
        async def wrapper(self, light_ip: str):
            try:
                light = wizlight(light_ip)
                result = await func(self, light)

                light_state = await light.updateState()
                light_status = light_state.get_state()

                ip_octet = get_ip_last_octet(light)

                states = [
                    {
                        "id": f"{PLUGIN_ID}.state.light.{ip_octet}.ip",
                        "description": f"WIZ | Light IP: {ip_octet}",
                        "value": str(light.ip),
                        "parentGroup": f"Light {ip_octet}"
                    },
                    {
                        "id": f"{PLUGIN_ID}.state.light.{ip_octet}.status",
                        "description": f"WIZ | Light Status: {ip_octet}",
                        "value": str(light_status),
                        "parentGroup": f"Light {ip_octet}"
                    }
                ]

                brightness = str(light_state.get_brightness())  # Getting Current Light Brightness
                if brightness != "None":
                    states.extend([
                        {
                            "id": f"{PLUGIN_ID}.state.light.{ip_octet}.brightness",
                            "description": f"WIZ | Light Brightness: {ip_octet}",
                            "value": str(light_state.__dict__['pilotResult']['dimming']),
                            "parentGroup": f"Light {ip_octet}"
                        },
                        {
                            "id": f"{PLUGIN_ID}.state.light.{ip_octet}.color_temp",
                            "description": f"WIZ | Light Color Temp: {ip_octet}",
                            "value": str(light_state.get_colortemp()),
                            "parentGroup": f"Light {ip_octet}"
                        },
                        {
                            "id": f"{PLUGIN_ID}.state.light.{ip_octet}.scene",
                            "description": f"WIZ | Light Scene: {ip_octet}",
                            "value": str(light_state.get_scene()),
                            "parentGroup": f"Light {ip_octet}"
                        }
                    ])

                # TPClient.createStateMany(states)

                TPClient.stateUpdateMany(states)

                g_log.info(f"{light_ip} - Light Status: {light_status}")
                return result
            except Exception as e:
                print("Error in update_light_state: ", e)
        return wrapper
    


    
    # def update_light_state(func):
    #     """ My first decorartor. It updates the light status after a light action is performed. """
    #     @wraps(func)
    #     async def wrapper(self, light_ip: str):
    #         try:
    #             light = wizlight(light_ip)
    #             result = await func(self, light)
                
    #             light_state = await light.updateState()
    #             light_status = light_state.get_state()
                
    #             # print(light_state.__dict__,"\n\n")
                
    #             ip_octet = get_ip_last_octet(light)
                
                
    #             ## Create an IP state if it doesnt exist
    #             TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".ip", description="WIZ | Light IP: " + str(ip_octet), value=str(light.ip), parentGroup=str("Light " + str(ip_octet)))
                
    #             ## Light Status
    #             TPClient.createState(f"{PLUGIN_ID}.state.light.{str(ip_octet)}.status", description="WIZ | Light Status: " + str(ip_octet), value=str(light_status), parentGroup=str("Light " + str(ip_octet)))
                
    #             brightness = str(light_state.get_brightness()) # Getting Current Light Brightness
    #             if brightness != "None":
    #                 ### Creating the state here because if its not found in list and user has CUSTOM Light set up then it wouldnt be created by default, so now it should make all states as expected.
    #                                         #    new_brightness = (int(brightness) / 255) * 100
    #                 ## Light Brightness
    #                 TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".brightness", description="WIZ | Light Brightness: " + str(ip_octet), value=str(light_state.__dict__['pilotResult']['dimming']), parentGroup=str("Light " + str(ip_octet)))
    #                 ## Color Temp
    #                 TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".color_temp", description="WIZ | Light Color Temp: " + str(ip_octet), value=str(light_state.get_colortemp()) , parentGroup=str("Light " + str(ip_octet)))
        
    #                 ## Current Scene Name
    #                 TPClient.createState(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", description="WIZ | Light Scene: " + str(ip_octet), value=str(light_state.get_scene()), parentGroup=str("Light " + str(ip_octet)))
                
    #             g_log.info(f"{light_ip} - Light Status: {light_status}")
    #             return result
    #         except Exception as e:
    #             print("this is the error: ", e)
    #     return wrapper
    
    
    @update_light_state
    async def light_on(self, light: wizlight):
        await light.turn_on()
        
    @update_light_state
    async def light_off(self, light: wizlight):
        await light.turn_off()
        
    @update_light_state
    async def light_toggle(self, light: wizlight):
        #await  light.set_ratio(0)
        await light.lightSwitch()


    async def set_light_speed(self, light_ip, speed: int):
        theLight: wizlight = self.bulb_type_dict[light_ip]['TheLight']
        await theLight.set_speed(speed)

    async def light_white(self, light_ip:str, brightness:int, kelvin:int = 3200)->None:
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
        
        # Turn on the light with the specified warm_white, cold_white, brightness, and color temperature values
        await light.turn_on(PilotBuilder(warm_white=0, cold_white=0, brightness=int(brightness * 2.55), colortemp=kelvin))
    
        # self.change_light_icon_color(light_ip=light_ip, color=COLOR_CODES2[str(kelvin)]['RGB'])


        kelvin_color = get_closest_kelvin(kelvin)
        self.change_light_icon_color(light_ip, kelvin_color)

        ip_octet = get_ip_last_octet(light)

        TPClient.stateUpdateMany([
            {
                "id": f"{PLUGIN_ID}.state.light.{ip_octet}.brightness",
                "value": str(brightness)
            },
            {
                "id": f"{PLUGIN_ID}.state.light.{ip_octet}.color_temp",
                "value": str(kelvin)
            },
            {
                "id": f"{PLUGIN_ID}.state.light.{ip_octet}.scene",
                "value": "None"
            }
        ])



    async def light_brightness(self, light_ip: str, brightness: int)->None:
        """
        Change the brightness of a light. 
        Used directly by the slider control.

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
        if light_ip in self.bulb_type_dict:
            theLight: wizlight = self.bulb_type_dict[light_ip]['TheLight']
            ip_octet = get_ip_last_octet(self.bulb_type_dict[light_ip]['TheLight'])
            if brightness <= 255:
                await theLight.turn_on(PilotBuilder(brightness=brightness))
                new_brightness = (int(brightness) / 255) * 100
                TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) + ".brightness", str(round(new_brightness)))

        else:
            print(f"No entry found for IP: {light_ip}", self.bulb_type_dict)





    async def light_color(self, light_ip:str, color: tuple)-> None:
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
            ip_octet = get_ip_last_octet(light)


            if self.bulb_type_dict[light_ip]['current_scene'] != None:
                threading.Thread(target=self.set_light_scene_icon, kwargs={'ip_octet': ip_octet, 'light_scene': "None"}).start()
                # self.set_light_scene_icon(ip_octet = ip_octet, light_scene = "None")
                self.bulb_type_dict[light_ip]['current_scene'] = None

            TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue="None")
            
            # Log the current color of the light
            g_log.info(f"{light_ip} | Current Color: "+ cur_color)




    async def light_scene(self, light_ip:str, scene_id:int)-> None:
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
        await light.turn_on(PilotBuilder(scene = scene_id))
    
        # Update the state of the light and get the name of the current scene
        state = await light.updateState()
        light_scene = state.get_scene()
        self.bulb_type_dict[light_ip]['current_scene'] = light_scene
        g_log.info(f"{light_ip} | Current Scene: "+ light_scene)
    
        # Get the index of the light and set its "scene" to the current scene using the TPClient.stateUpdate method
       # index = controller.get_light_index(light_ip)
        ip_octet = get_ip_last_octet(light)
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".scene", stateValue=light_scene)
        self.set_light_scene_icon(ip_octet, light_scene)




    async def light_effect(self, light_ip: str, speed: int)->None:
        """
        Set the speed of a light's effect.
        
        Parameters:
            light_ip (str): IP address of the light.
            speed (int): Speed of the light's effect, from 10 to 200.
            
        Returns:
            None
            
        Notes:
            - The `speed` parameter should be an integer value between 10 and 200.
            - If the `speed` parameter is less than 10, it will be set to 10.
            - If the `speed` parameter is greater than 200, it will be set to 200.
        """
        light = wizlight(light_ip)
        set_speed = max(10, min(speed, 200))
        await light.set_speed(set_speed)
        ip_octet = get_ip_last_octet(light)
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) + ".effect_speed", stateValue=str(set_speed))




    async def get_light_color(self, light: wizlight)-> tuple:
        """
        Get the current color of a light at the specified IP address.
        Parameters:
        - light_ip: The IP address of the light to get the color of.
        
        Returns:
        A tuple containing the RGB values of the light's current color, in the range 0-255.
        """
        
        # Create a wizlight object for the light at the given IP address
        # light = wizlight(light_ip)
        # Update the state of the light and get the RGB values
        state = await light.updateState()
        red, green, blue = state.get_rgb()
        
        # Return the RGB values as a tuple
        return (red, green, blue)



    def change_light_icon_color(self, light_ip:str, color: tuple, onstart=None)-> str:
        """ 
        This function changes the icon color for the light set at that Index
        """
        
        ### convert rgb tuple to hex
        try:
            ahex = '%02x%02x%02x' % color
        except TypeError:
            color = tuple(map(int, color))
            ahex = '%02x%02x%02x' % color
            
        aarrggbb = f'#FF{ahex}'

        if onstart:
            ip_octet = get_ip_last_octet(light_ip, onstart)
        else:
            ip_octet = get_ip_last_octet(self.bulb_type_dict[light_ip]['TheLight'], onstart)
            
        TPClient.stateUpdate(PLUGIN_ID + ".state.light." + str(ip_octet) +".icon_color", stateValue=aarrggbb)
        return aarrggbb





################################### UTIL STYLE THINGS

 #  def get_light_index(self, light_ip:str):
 #      """ 
 #      This function gets the index of the light in the bulb_type_dict
 #      """
 #      index = list(controller.bulb_type_dict.keys()).index(light_ip)
 #      return index
    
    
    def update_choices(self, bulb_type_dict:dict)-> None:
        """ 
        This function updates the choices for the light selection. 
        """
        IP_LIST = organize_ips(list(bulb_type_dict.keys()))
        IP_LIST.append("Custom")
        TPClient.choiceUpdate(PLUGIN_ID + ".act.light.selection",
                              values=list(IP_LIST))
        TPClient.choiceUpdate(PLUGIN_ID + ".connector.light.brightnessControl.choices",
                              values=list(IP_LIST))
