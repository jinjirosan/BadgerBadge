# A badge for the little one

For a while I was looking to build a badge using a Raspberry Pi Zero and a Waveshare e-INK display. Everything I tried, it was just to bulky and heavy. Then the awesome people at Pimoroni came out with the badger2040 platform. Exactly what I needed!

Well almost, I added a couple of things to make it practical for my purposes.  The badge has the following functions:

- Badge : name, photo and my contact number
- List : a simple listing of the items my kid takes to school
- Image : a couple of photos of us together
- Timer : an activity countdown timer with 6 selectable activities and preset times
- Temp : displays the current temperature, humidity, pressure and shows descriptions on the weather
- Elevation : measure height in meters and floors

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

The SigFox module will be used to send periodic messages back on status. Added bonus is that each received SigFox message has a (very broad) position indication which covers all of Europe. You get a rough idea where the badge is (search area as large as the City of The Hague).

### Images of the GUI and functions

![GUI](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_2.jpg)
###### --> image: First menu page showing the first three functions

![badge](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_3.jpg)
###### --> image: The badge itself

![list](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_7.jpg)
###### --> image: The list

![GUI](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_8.jpg)
###### --> image: The second menu page showing the last three functions. (customized icones :-) )

![timer](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_6.jpg)
###### --> image: The timer app showing the activity list

![timer](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_9.jpg)
###### --> image: The timer app showing the countdown

![temp](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_4.jpg)
###### --> image: the temperature app

![elevation](https://github.com/jinjirosan/BadgerBadge/blob/main/images/im_5.jpg)
###### --> image: The elevation app
