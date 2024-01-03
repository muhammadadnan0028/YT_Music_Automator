from uiautomator2 import Device
import time
from itertools import count

def interact_with_instagram(emulator_name):
    device = Device(emulator_name)
    device.session('com.Ytmusic.android')


    time.sleep(6)
