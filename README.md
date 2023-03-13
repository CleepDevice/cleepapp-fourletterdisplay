# Fourletterdisplay [![Coverage Status](https://coveralls.io/repos/github/CleepDevice/cleepapp-fourletterdisplay/badge.svg)](https://coveralls.io/github/CleepDevice/cleepapp-fourletterdisplay)

Four-letter pHAT Cleep driver for [Piromoni hardware](https://shop.pimoroni.com/products/four-letter-phat).

![alt text](https://github.com/CleepDevice/cleepapp-fourletterdisplay/blob/master/resources/phat.jpg?raw=true "Piromoni Four-letter pHAT")

Install python library and render basic events (time). It also implements functions to display text on segments.

## Installation

Solder the 40-pin header and the 2 digits on the board then plug it into your raspberry-pi and install this application on Cleep.

## Configuration

Once app installed hardware is ready to use.

With configuration page you can:
* configure default digit brightness
* enable night mode to reduce brightness after sunset.
* send text to test the display

## Gpios

This hardware uses 2 raspberry pi gpios. See list [here](https://pinout.xyz/pinout/four_letter_phat).
So it is possible to connect other hardware that doesn't need those gpios

