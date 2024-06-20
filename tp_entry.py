__version__ = 100
PLUGIN_ID = "tp.plugin.WizLights"
PLUGIN_NAME = "WizLight"
PLUGIN_FOLDER = "WizLight"

import socket
import ipaddress

def get_broadcast_address():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connect to a remote server
    s.connect(("8.8.8.8", 80))

    # Get the local IP address
    local_ip = s.getsockname()[0]

    # Calculate the broadcast address
    ip_interface = ipaddress.ip_interface(f"{local_ip}/24")
    broadcast_address = ip_interface.network.broadcast_address

    return str(broadcast_address)

print(get_broadcast_address())
TP_PLUGIN_INFO = {
    'sdk': 6,
    'version': __version__,  # TP only recognizes integer version numbers
    'name': f"{PLUGIN_NAME} Plugin",
    'id': PLUGIN_ID,
    "plugin_start_cmd_windows": f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\{PLUGIN_NAME}_Plugin.exe",
  # "plugin_start_cmd_linux": "sh %TP_PLUGIN_FOLDER%YouTube_Plugin//start.sh TP_YouTube_Plugin",
  #  "plugin_start_cmd_mac": "sh %TP_PLUGIN_FOLDER%YouTube_Plugin//start.sh TP_YouTube_Plugin",
    'configuration': {
        "colorDark": "#23272a", ##23272a
        "colorLight": "#57ad72" 
    }
}



TP_PLUGIN_SETTINGS = {
    
    'Broadcast IP Address': {
        'name': "Local Broadcast IP",
        'type': "text",
        'default': "",
        'readOnly': False,
        'value': None  
    }
}




TP_PLUGIN_CATEGORIES = {
    "main": {
        'id': PLUGIN_ID + ".main",
        'name' : "WizLight",
        'imagepath': f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\wizlight_w.png",
    }
}


TP_PLUGIN_ACTIONS = {
    'Turn On / Off Light': {
        'category': "main",
        'id': PLUGIN_ID + ".act.turn.on.off.light",
        'name': "WIZ | Turn On / Off Light",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Select a Light to Turn On / Off",
        'format': "$[1]  Light:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'On/Off/Toggle': {
                'id': PLUGIN_ID + ".act.light.on.off.toggle",
                'type': "choice",
                'label': "Text",
                'default': "Toggle",
                "valueChoices": ["On", "Off", "Toggle"]
        },
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Light Brightness': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.brightness",
        'name': "WIZ | Light Brightness",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Brightness of a Light",
        'format': "Light:$[1] Brightness:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        "Light Brightness": {
            "id": PLUGIN_ID + ".act.light.brightness.choice",
            "type": "text",
            "label": "Brightness",
            "default": "100",
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
        
    },
    'Light Color RGB': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.color.rgb",
        'name': "WIZ | Change Light Color (RGB)",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Color of a Light",
        'format': "Light:$[1]  Color:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Color Choice': {
                'id': PLUGIN_ID + ".act.light.color_selector",
                'type': "color",
                'label': "Text",
                'default': "",
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Light Color RGB (MANUAL)': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.color.rgb.manual",
        'name': "WIZ | Change Light Color (RGB-Manual)",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Color of a Light",
        'format': "Light:$[1]  R:$[2] G:$[3]  B:$[4]  | CUSTOM LIGHT(optional): $[5]",
        'data': {
        'Light Selection': {
            'id': PLUGIN_ID + ".act.light.selection",
            'type': "choice",
            'label': "Text",
            'default': "",
            "valueChoices": []
        },
            'Red': {
                "id": PLUGIN_ID + ".act.light.color.rgb.manual.red",
                "type": "number",
                "label": "Red",
                "default": 0,
                "min": 0,
                "max": 255,
                  
            },
            'Green': {
                "id": PLUGIN_ID + ".act.light.color.rgb.manual.green",
                "type": "number",
                "label": "Green",
                "default": 0,
                "min": 0,
                "max": 255,
            },
            'Blue': {
                "id": PLUGIN_ID + ".act.light.color.rgb.manual.blue",
                "type": "number",
                "label": "Blue",
                "default": 0,
                "min": 0,
                "max": 255,
                  
            },
            'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
        'Light Scene Selection': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.scene_select",
        'name': "WIZ | Change Light Scene",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Scene of a Light",
        'format': "Light:$[1]  Scene:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Scene Choice': {
                'id': PLUGIN_ID + ".act.light.scene_select.choice",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Set Light White': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.set_white",
        'name': "WIZ | Change Light to White (Warm/Cool)",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Color of a Light to Cold or Warm White  - Brightness is 0-100",
        'format': "Light:$[1] Brightness:$[2] Kelvin:$[3] | CUSTOM LIGHT(optional): $[4]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        # 'Light Choice': {
        #         'id': PLUGIN_ID + ".act.light.set_white.type",
        #         'type': "choice",
        #         'label': "Text",
        #         'default': "",
        #         'valueChoices': ["Warm White", "Cold White", "Daylight"]
        # },
        'Light Choice Brightness': {
                'id': PLUGIN_ID + ".act.light.set_white.brightness",
                'type': "text",
                'label': "Text",
                'default': "100"
        },
        "Kelvin Range": {
                "id": PLUGIN_ID + ".act.light.set_white.kelvin",
                'type': "choice",
                'label': "Text",
                'default': "3500",
                'valueChoices': ["None", "2200", "2700", "3000", "3100", "3500", "4100", "5000", "5500", "6500"]
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Light Scene Selection': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.scene_select",
        'name': "WIZ | Change Light Scene",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change the Scene of a Light",
        'format': "Light:$[1]  Scene:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Scene Choice': {
                'id': PLUGIN_ID + ".act.light.scene_select.choice",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Light Effect Speed': {
        'category': "main",
        'id': PLUGIN_ID + ".act.light.effect_speed",
        'name': "WIZ | Change Light Effect Speed",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Change Effect Speed of a Light - Min:10 Max:200",
        'format': "Light:$[1]  Effect Speed:$[2]  | CUSTOM LIGHT(optional): $[3]",
        'data': {
        'Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        },
        'Effect Speed': {
                'id': PLUGIN_ID + ".act.light.effect_speed.choice",
                'type': "text",
                'label': "Text",
                'default': "",
        },
        'Custom Light Selection': {
                'id': PLUGIN_ID + ".act.light.selection.custom",
                'type': "text",
                'label': "Text",
                'default': "",
        }
        }
    },
    'Discover New Lights': {
        'category': "main",
        'id': PLUGIN_ID + ".act.discover.new_lights",
        'name': "WIZ | Discover New Lights",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        "description": "Discover New Lights on Network",
        'format': "Discover New Lights on the Network",
        'data': {
        'Discovery Action': {
                'id': PLUGIN_ID + ".act.light.filler",
                'type': "choice",
                'label': "Text",
                'default': "",
                "valueChoices": []
        }
        }
    }
}


TP_PLUGIN_STATES = {
    'Status': {
        'category': "main",
        'id': PLUGIN_ID + ".state.plugin_status",
        'desc': "Wiz | Plugin Status",
        'default': ""
    },
    'Time-Running': {
        'category': "main",
        'id': PLUGIN_ID + ".state.time_running",
        'desc': "Wiz | Time Running",
        'default': ""
    }
}


TP_PLUGIN_CONNECTORS = {
    "Brightness Control": {
        'category': "main",
        "id": PLUGIN_ID + ".connector.light.brightnessControl",
        "name": "Brightness Slider",
        "format": "Adjust Brightness for $[1]  | CUSTOM LIGHT(optional): $[2]",
        "label": "Adjust Light Brightness",
        "data": {
            "brightness": {
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices",
                "type": "choice",
                "label": "",
                "default": "",
                "valueChoices": []
            },
            "custom device": {
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices.custom",
                "type": "text",
                "label": "",
                "default": "",
            }
        }
    },
    
    "Slider Control": {
        'category': "main",
        "id": PLUGIN_ID + ".connector.light.AllControl",
        "name": "Custom Light Slider",
        "description": "Custom Options include: Brightness, Color, White",
        "format": "Adjust $[1] for $[2]  | CUSTOM LIGHT(optional): $[3]",
        "label": "Adjust Light Color, Brightness, or White Shade",
        "data": {
            "Slider Choice": {
                "id": PLUGIN_ID + ".connector.light.AllControl.choices.slider",
                "type": "text",
                "label": "",
                "default": "",
            },
            "Light IPs": { ## ths is actually the IP.... 
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices",
                "type": "choice",
                "label": "",
                "default": "",
                "valueChoices": []
            },
            "custom device": {
                "id": PLUGIN_ID + ".connector.light.AllControl.choices.custom",
                "type": "text",
                "label": "",
                "default": "",
            },

        }
    },
    "Hue Changer": {
        'category': "main",
        "id": PLUGIN_ID + ".connector.light.hueControl",
        "name": "Hue Slider",
        "format": "Adjust Hue for $[1]  | CUSTOM LIGHT(optional): $[2]",
        "label": "Adjust Light Hue",
        "data": {
            "brightness": {
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices",
                "type": "choice",
                "label": "",
                "default": "",
                "valueChoices": []
            },
            "custom device": {
                "id": PLUGIN_ID + ".connector.light.hueControl.choices.custom",
                "type": "text",
                "label": "",
                "default": "",
            }
        }
    },
    "White Changer": {
        'category': "main",
        "id": PLUGIN_ID + ".connector.light.whiteControl",
        "name": "White Slider",
        "format": "Adjust White for $[1]  | CUSTOM LIGHT(optional): $[2]",
        "label": "Adjust Light White",
        "data": {
            "default choices": {
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices",
                "type": "choice",
                "label": "",
                "default": "",
                "valueChoices": []
            },
            "custom device": {
                "id": PLUGIN_ID + ".connector.light.whiteControl.choices.custom",
                "type": "text",
                "label": "",
                "default": "",
            }
        }
    },
    "Speed Changer": {
        'category': "main",
        "id": PLUGIN_ID + ".connector.light.speedControl",
        "name": "Effect Speed Slider",
        "format": "Adjust Speed for $[1]  | CUSTOM LIGHT(optional): $[2]",
        "label": "Adjust Light Effect Speed",
        "data": {
            "default choices": {
                "id": PLUGIN_ID + ".connector.light.brightnessControl.choices",
                "type": "choice",
                "label": "",
                "default": "",
                "valueChoices": []
            },
            "custom device": {
                "id": PLUGIN_ID + ".connector.light.speedControl.choices.custom",
                "type": "text",
                "label": "",
                "default": "",
            }
        }
    }
}


TP_PLUGIN_EVENTS = {
    "0": {
        'id': PLUGIN_ID + ".event.user_0.speaking",
        'name':"DC | User 0 - Speaking",
        'category': "main",
        "format":"When User 0 is speaking - $val",
        "type":"communicate",
        "valueType":"choice",
        "valueChoices": [
            "True",
            "False"
            ],
        "valueStateId": PLUGIN_ID + ".state.User_0.speaking",
		}
}



