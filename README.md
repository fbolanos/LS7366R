# LS7366R
A simple python library to interface the Raspberry Pi with the LS7366R IC.

To run the simple test application run the LS7366R.py script.
You should be able to import this class easily within some other main script.
Using this library I was able to comfortably reach a sampling rate of at least 125Hz with the Raspberry Pi 2.
Now that the Raspberry Pi 4 is available I bet you can sample much much faster.

If speed in the KHz is needed, you will have to use C++.

Make sure the Pi has spidev installed, and that SPI is enabled.

P.S. I originally wrote this back when I was starting to learn OOP... so it probably doesn't follow all the conventions properly.

Dependencies:
* python3
* spidev




