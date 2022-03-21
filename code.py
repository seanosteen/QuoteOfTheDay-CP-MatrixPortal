# Quote of the Day Scrolling Display
# uses the MatrixPortal webservice fetch and json parsing to display a random quote from ZenQuotes.io
# Code based on the Adafruit Quote Board sample y John Park
# (https://learn.adafruit.com/aio-quote-board-matrix-display/code-the-quote-board)

import time
import random
import terminalio
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_matrixportal.matrixportal import MatrixPortal
import supervisor

# --- Display setup ---
matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    debug=True,
    rotation=180)

FONT = "/IBMPlexMono-Medium-24_jep.bdf"

# Create a new label with the color and text selected
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,
)

# Static 'Connecting' Text
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)

SCROLL_DELAY = 0.04
UPDATE_DELAY = 600

quotes = ['No Quotes Found']
colors = ['#FF0000', '#00FF00', '#0000FF']
last_color = None
last_quote = None


def update_data():
    print("Updating data from ZenQuotes")
    matrixportal.set_text("Updating...", 1)

    try:
        quotes_data = matrixportal.network.fetch('https://zenquotes.io/api/random')
        quotes.clear()
        for json_data in quotes_data.json():
            quotes.append('"{0}" - {1}'.format(json_data['q'], json_data['a']))
        print(quotes)
    # pylint: disable=broad-except
    except Exception as error:
        print(error)
        supervisor.reload()

    if not quotes or not colors:
        raise RuntimeError("Please add at least one quote and color to your feeds")
    matrixportal.set_text(" ", 1)


update_data()
last_update = time.monotonic()
matrixportal.set_text(" ", 1)
quote_index = None
color_index = None

while True:
    # Choose a random quote from quotes
    if len(quotes) > 1 and last_quote is not None:
        while quote_index == last_quote:
            quote_index = random.randrange(0, len(quotes))
    else:
        quote_index = random.randrange(0, len(quotes))
    last_quote = quote_index

    # Choose a random color from colors
    if len(colors) > 1 and last_color is not None:
        while color_index == last_color:
            color_index = random.randrange(0, len(colors))
    else:
        color_index = random.randrange(0, len(colors))
    last_color = color_index

    # Set the quote text
    matrixportal.set_text(quotes[quote_index])

    # Set the text color
    matrixportal.set_text_color(colors[color_index])

    # Scroll it
    matrixportal.scroll_text(SCROLL_DELAY)

    if time.monotonic() > last_update + UPDATE_DELAY:
        update_data()
        last_update = time.monotonic()
