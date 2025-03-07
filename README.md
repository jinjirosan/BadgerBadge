# A badge for the little one

For a while I was looking to build a badge using a Raspberry Pi Zero and a Waveshare e-INK display. Everything I tried, it was just to bulky and heavy. Then the awesome people at Pimoroni came out with the badger2040 platform. Exactly what I needed!

Well almost, I added a couple of things to make it practical for my purposes.  The badge has the following functions:

- Badge : name, photo and my contact number
- List : a simple listing of the items my kid takes to school
- Image : a couple of photos of us together
- Timer : an activity countdown timer with 6 selectable activities and preset times
- Temp : displays the current temperature, humidity, pressure and shows descriptions on the weather
- Elevation : measure height in meters and floors
- Focus : a Pomodoro-like timer in traffic light. Presets on Red time (focus, don't disturb) and Orange (can whisper, be slightly distracted) time
- Medical : shows a quick overview of essentials such as Blood Type, Weight, Height, Age, Allergies and Medications
- Help/SOS : displays a list of emergency contacts and numbers (used to have this on a laminated card)
- Comms : an experimental app using the Sigfox bi-directional messages capability to also display downlink messages

The badge is now on Hardware Prototype Platform v3

![Hardware Prototype Platform v3](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_1.jpg)
###### --> image: Hardware Prototype Platform v3

| Function    | Board           | Description  |
|:------------- |:-------------|:-----|
| Charging circuit   | LiPo Amigo  | Badger does not have a charging circuit on-board  |
| Power    | 150 mAh LiPo |This is perfect size-wise and capacity lasts a while | 
| Temp, Hum, Press, Gas     | BME680 | Perfect little sensor for weather stuff   |
| Communications SigFox 868Mhz	 | LPWAN SigFox Node     | used to send 140 12-byte daily messages   |
| Antenna uFL 850Mhz | flat sticker antenna      |Smallest, flattest antenna I could find   |

The SigFox module will be used to send periodic messages back on status. Added bonus is that each received SigFox message has a (very broad) position indication which covers all of Europe. You get a rough idea where the badge is.

### The (rough) area of the badge location

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_17.png)
###### --> image: We took the badge on a weekendtrip to Antwerpen Zoo

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_18.png)
###### --> image: We took the badge on a trip to Berlin

### Images of the GUI and functions

![GUI](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_2.jpg)
###### --> image: First menu page showing the first three functions

![badge](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_3.jpg)
###### --> image: The badge itself

![list](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_16.jpg)
###### --> image: The list

![GUI](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_8.jpg)
###### --> image: The second menu page showing the last three functions. (customized icones :-) )

![timer](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_6.jpg)
###### --> image: The timer app showing the activity list

![timer](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_9.jpg)
###### --> image: The timer app showing the countdown

![temp](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_12.jpg)
###### --> image: the temperature app

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_5.jpg)
###### --> image: The elevation app

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_10.jpg)
###### --> image: The focus app, menu

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_11.jpg)
###### --> image: The focus app, countdown and traffic light change

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_13.jpg)
###### --> image: menu items : Focus, Medical and Help/SOS

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_15.jpg)
###### --> image: The Medical app, quick overview of essential info (showing fake data here)

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_14.png)
###### --> image: The Help app, showing important contacts and their phone numbers

