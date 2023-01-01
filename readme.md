
# WizLight-Plugin

![image](https://user-images.githubusercontent.com/76603653/210160506-9788db10-5221-4709-a9c2-671027a4fd7b.png)


- [WizLight Plugin](#WizLight-Plugin)
  - [Description](#description) 
  - [Settings Overview](#Settings-Overview)
  - [Features](#Features)
    - [Actions](#actions)
        - [Category: WizLight](#tp.plugin.WizLights.mainactions)
    - [Connectors](#connectors)
        - [Category: WizLight](#tp.plugin.WizLights.mainconnectors)
    - [States](#states)
        - [Category: WizLight](#tp.plugin.WizLights.mainstates)
    - [Events](#events)
        - [Category: WizLight](#tp.plugin.WizLights.mainevents)
  - [Bugs and Support](#bugs-and-suggestion)
  - [License](#license)
  
# Description

This documentation generated for WizLight Plugin V100 with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).

## Settings Overview
| Read-only | Type | Default Value |
| --- | --- | --- |
| False | text |  |


# Features

## Actions
<details open id='tp.plugin.WizLights.mainactions'><summary><b>Category:</b> WizLight <small><ins>(Click to expand)</ins></small></summary><table>
<tr valign='buttom'><th>Action Name</th><th>Description</th><th>Format</th><th nowrap>Data<br/><div align=left><sub>choices/default (in bold)</th><th>On<br/>Hold</sub></div></th></tr>
<tr valign='top'><td>WIZ | Turn On / Off Light</td><td> </td><td>[1]  Light:[2]  | CUSTOM LIGHT(optional): [3]</td><td><ol start=1><li>Type: choice &nbsp; 
Default: <b>Toggle</b> Possible choices: ['On', 'Off', 'Toggle']</li>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>WIZ | Light Brightness</td><td> </td><td>Light:[1] Brightness:[2]  | CUSTOM LIGHT(optional): [3]</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
Default: <b>100</b></li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>WIZ | Change Light Color (RGB)</td><td> </td><td>Light:[1]  Color:[2]  | CUSTOM LIGHT(optional): [3]</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: color &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>WIZ | Change Light Color (RGB-Manual)</td><td> </td><td>Light:[1]  R:[2] G:[3]  B:[4]  | CUSTOM LIGHT(optional): [5]</td><td><details><summary><ins>Click to expand</ins></summary><ol start=1>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: number &nbsp; 
Default: <b>0</b> &nbsp; <b>Min Value:</b> -2147483648 &nbsp; <b>Max Value:</b> 2147483647</li>
<li>Type: number &nbsp; 
Default: <b>0</b> &nbsp; <b>Min Value:</b> -2147483648 &nbsp; <b>Max Value:</b> 2147483647</li>
<li>Type: number &nbsp; 
Default: <b>0</b> &nbsp; <b>Min Value:</b> -2147483648 &nbsp; <b>Max Value:</b> 2147483647</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</details><td align=center>No</td>
<tr valign='top'><td>WIZ | Change Light Scene</td><td> </td><td>Light:[1]  Scene:[2]  | CUSTOM LIGHT(optional): [3]</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>WIZ | Change Light to White (Warm/Cool)</td><td> </td><td>Light:[1]  Light Type:[2], Brightness:[3] Kelvin:[4] | CUSTOM LIGHT(optional): [5]</td><td><details><summary><ins>Click to expand</ins></summary><ol start=1>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: choice &nbsp; 
Default: <b></b> Possible choices: ['Warm White', 'Cold White', 'Daylight']</li>
<li>Type: text &nbsp; 
Default: <b>100</b></li>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</details><td align=center>No</td>
<tr valign='top'><td>WIZ | Change Light Effect Speed</td><td> </td><td>Light:[1]  Effect Speed:[2]  | CUSTOM LIGHT(optional): [3]</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>WIZ | Discover New Lights</td><td> </td><td>Discover New Lights on the Network</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
</tr></table></details>
<br>

## Connectors
<details open id='tp.plugin.WizLights.mainconnectors'><summary><b>Category:</b> WizLight <small><ins>(Click to expand)</ins></small></summary><table>
<tr valign='buttom'><th>Slider Name</th><th>Description</th><th>Format</th><th nowrap>Data<br/><div align=left><sub>choices/default (in bold)</th></tr>
<tr valign='top'><td>Hue Slider</td><td> </td><td>Adjust Hue for [1]  | CUSTOM LIGHT(optional): [2]</td><td><ol start=1><li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</table></details>
<br>

## States
<details open id='tp.plugin.WizLights.mainstates'><summary><b>Category:</b> WizLight <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .state.plugin_status | Wiz | Plugin Status |  |   |
| .state.time_running | Wiz | Time Running |  |   |
</details>

<br>

## Events

<td></tr>
<details open id='tp.plugin.WizLights.mainevents'><summary><b>Category: </b>WizLight <small><ins>(Click to expand)</ins></small></summary>

<table>
<tr valign='buttom'><th>Id</th><th>Name</th><th nowrap>Evaluated State Id</th><th>Format</th><th>Type</th><th>Choice(s)</th></tr>
<tr valign='top'><td>.event.user_0.speaking</td><td>DC | User 0 - Speaking</td><td>.state.User_0.speaking</td><td>When User 0 is speaking - $val</td><td>choice</td><td><ul><li>True</li><li>False</li></ul></td></table></details>
<br>

# Bugs and Suggestion
Open an issue on github or join offical [TouchPortal Discord](https://discord.gg/MgxQb8r) for support.


# License
This plugin is licensed under the [GPL 3.0 License] - see the [LICENSE](LICENSE) file for more information.

