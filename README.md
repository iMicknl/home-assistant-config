# Home Automation - MC
The full Home Automation config of Mick & Cris.

### Hardware
* Raspberry Pi 3
* Z-Wave Z-Stick Gen5

### Software
* HomeAssistant
* NGINX

### Components
1. Lights
    * Philips Hue Hub
    * Philips Hue Color - x11 (connected via Philips Hue Hub)
    * Ikea Tradfri White - x1 (connected via Philips Hue Hub)
    * Ikea Tradri Color - x3 (connected via Philips Hue Hub)
1. Camera
    * Foscam C2
1. MediaPlayers
    * LG TV 44UJ635V
    * Apple TV 4K
    * Sonos PlayBase
    * Harman Kardon Invoke (Cortana)
    * Amazon Echo Spot (Alexa)
1. Device Tracker
    * Asus RT-AC5300
1. Vacuum Cleaners
    * Xiaomi Vacuum 1
1. Sensors (physical)
    * Xiaomi Mi Flora Plant sensor - x3
    * Neo CoolCam Door/Window Detector (Z-Wave)
    * Schlage Link Mini Keypad RFID (Z-Wave)
    * Aeotec ZW100 MultiSensor 6 (Z-Wave)
    * Neo CoolCam MultiSensor (Z-Wave)
    * Energy Usage (via smart meter and P1 cable)
1. Sensors (digital)
    * Packages (PostNL)
    * Weather (BuienRadar)
    * Speedtest (Ookla)
    * SSL certificate expiry

### Interfaces
* Web (via custom domain)
* iOS app + push
* HomeKit 
* Alexa

### Automation
1. Turn on the lights when someone comes home
1. Turn on the lights in the hallway when door is opened
1. Turn on the lights when motion is detected in the corridor 
1. Notify everyone when front door is open 1+ minutes
1. Turn lights off when Mick leaves home

## Screenshots (web)
![Overview](/docs/screenshots/overview.png?raw=true "Overview")
![Gang](/docs/screenshots/gang.png?raw=true "Gang")
![Woonkamer](/docs/screenshots/woonkamer.png?raw=true "Woonkamer")
![Mick](/docs/screenshots/mick.png?raw=true "Mick")
![Stats](/docs/screenshots/stats.png?raw=true "Stats")
