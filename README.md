# arduino_opsgenie_rgb
An Arduino LED Strip controller that bases the color on your opsgenie environment status.

### Circuit Design

Special thanks to https://www.makeuseof.com/tag/connect-led-light-strips-arduino/ where I first found the circuit design.

### Installation

This was designed for a Arduino Yun Rev2 but should be adaptable to other boards. The Python script itself is adaptable to a wide range of applications.
That said the instructions are written here with the Yun in mind.

1. Make sure you've setup your Yun to use an external sd and a swap file. The swap file is necessary to allow for getting the required packages.
2. Ensure PIP is installed following the instructions here: https://pip.pypa.io/en/stable/installing/
3. Run `python -m pip install requests`
4. Rename the `apikey.cfg.example` file to `apikey.cfg` and input your Opsgenie API Key (I recommend a read only key of course)
5. Upload the `opsgeniergb` folder which now includes `main.py` and your version of `apikey.cfg` to /mnt/sda1/pythonfiles/
6. Upload the sketch located in arduino_sketch to your yun.

### Troubleshooting

On boot once the yun bridge is available it will run through red,green,blue, and 50% white to confirm all your colors work and it is now waiting on the python script. If you don't see these lights one of your wires is probably set wrong.

The python script will be kicked off every 5 seconds. If there are problems reaching OpsGenie your lights will go purple. This will be common for the first few seconds after the LED Test as it fails waiting on the network processes. 

While the Python script is running the L13 light will be on. So normal behavior would be to see it regularly flashing on your board.

If it is regularly flashing, it is only green, but your colors aren't changing as expected ensure your API key has access to the incidents/alerts you are trying to setup.
