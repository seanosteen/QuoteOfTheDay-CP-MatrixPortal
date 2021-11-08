![Scrolling LED matrix using the ZenQuotes API](assets/ZenQuote-Scroller.gif)

# Quote of the Day Scroller - A Skill Builder for Circuit Python, Web Service APIs, and Electronics

## Overview

I'm a big fan of electronic billboards and stock ticker symbol displays. So, when I'm learning a new platform like Arduino *([1](https://github.com/seanosteen/IRC-Scrolling-Text-Bot) & [2](https://github.com/seanosteen/LED_SIGN_on_LOL_SHIELD_ANY_LENGTH))*, Raspberry Pi *([3](https://tinkeringrocks.com/2016/01/23/raspberry-pi-ntp-server-using-gps/) & [4](https://tinkeringrocks.com/2013/11/19/raspberry-pi-rs232-oauth/))*, or Circuit Python, one of the first projects I tend to make is some form of a textual information display.

Our good friends at [Adafruit](https://www.adafruit.com/product/4745) recently released a fantastic microcontroller platform specifically for their LED matrix products. The [MatrixPortal](https://www.adafruit.com/product/4745) is a rather beefy microcontroller with an ESP32 co-processor to make the network connectivity through WiFi, a breeze. I used this platform to create my first IoT project on Circuit Python. Adafruit already has some amazing getting started guides. I strongly recommend you give them a runthrough if you are a newbie to Circuit Python and their LED matrices. Once you have your Hello World project under your belt, I hope you find this sample program below helpful in turning your tinkering project into an information display!


## What You Will Need

I'm including the list of parts that I used and some important notes to help you over some of the stumbling blocks that I encountered along my journey. This isn't the only way to go about it, but this will at least get you to a working code example.

![LED MatrixPortal example](assets/MatrixPortal1.jpg)

**Parts:**

- [Adafruit 64x32 LED Matrix](https://www.adafruit.com/product/2277) - This is the LED display. They come is different shapes and sizes.  You can even chain several together to create larger displays.
- [Adafruit MatrixPortal - Circuit Python Powered Internet Display](https://www.adafruit.com/product/4745) - This is the brains behind the lights.  Adfruit created this clever board that contains both the microcontroller and the network connectivity into a package that plugs right into the back of their displays without the need for soldering or breadboarding!
- [5 Volt, 10 Amp Power Supply](https://www.amazon.com/gp/product/B0852HL336/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) - *Optional* - The MatrixPortal is capable of powering an LED matrix display through its USB-C port, so long as you don't have too many of the LEDs lit up at once.  However, if you have multiple LED matrices chained together, or you are planning to turn on all of the LEDs at once, you'll need to power the LEDs from an external source like this one. If you are powering by the USB-C port and you see any flickering or weird errors, you will need to power the LEDs externally.

**Software:**

- **A Code or Text Editor** - You are going to be pushing python code from your PC onto the MatrixPortal to run as a loop.  You can use your favorite IDE or text editor to do this, but the folks at Circuit Python recommend the [Mu Editor](https://codewith.mu/) which provides a couple of key advantages:
  - It has context-aware inline editing. I'm a sucker for a good auto completion tool.
  - It has a built-in serial console that can read the Circuit Python's standard out data. Very useful while debugging.

- **The Latest Build of Circuit Python** - CP is under constant and rapid development. The code in this project was written against Circuit Python V7.0.0. I strongly recommend you update your microcontroller with the latest version of Circuit Python before you begin.  Initially I had a lot of broken library links and attribute not found errors.  Once I flashed the MatrixPortal with the latest version of CircuitPython, all of those issues went away.
 - [How to install Circuit Python](https://learn.adafruit.com/matrix-portal-new-guide-scroller/install-circuitpython)
 - [Latest versions for the MatrixPortal](https://circuitpython.org/board/matrixportal_m4/)

## Connecting to the Internet

The MatrixPortal library has a very nice built-in WiFi library. It spawns a background task on the ESP chip that maintains the WiFi connection as needed. In order to take advantage of this built-in library for your connectivity and for web service calls, you will need to create a secrets.py file in the root directory of your Circuit Python drive:

**Sample secrets.py:**

```
# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it

secrets = {
    'ssid' : '<YOUR WIFI SSID NAME>',
    'password' : '<YOUR WIFI PASSPHRASE',
    'timezone' : "America/Los_Angeles" # http://worldtimeapi.org/timezones
    }

```


## About Using Bitmap Fonts

One of my hopes is to incorporate larger fonts into this Quote of the day board. The MatrixPortal library does allow for custom fonts. There's even an excelent tutorial available to use it. However, in practice, I found that the MatrixPortal encounters memory allocation errors once the quote string grows beyond 50 characters.  In the included code, we're just using the built in terminal font to display the quotes. However, if you are using only short text strings in your web service feed, you may be able to use the prettier fonts. If you want to play around with the included "IBMPlexMono-Medium-24_jep.bdf" font file, you can change one line of code as follows:

**From:**
```
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)
```

**To:**
```
matrixportal.add_text(
    text_font=FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)
```
