import os
import signal
import threading
import time

import keyboard
import mouse as m
from pynput import mouse

from guns.gun_detection.detect_gun import detect_gun
from guns.gun_detection.setup_data.load_data import load_data
from mouse_events.pull_down import mouse_pull_down

training_data = load_data(os.getcwd() + '/data')
equipped_gun = detect_gun(training_data)
puller = mouse_pull_down()


def mouse_handler(call):
    # if scroll wheel detected, then kick off gun detection
    if isinstance(call, m.WheelEvent):
        time.sleep(0.05)
        puller.equipped_gun = equipped_gun.detect()


def keyboard_handler(call):
    # if e is pressed, kick off gun detection
    time.sleep(0.05)
    puller.equipped_gun = equipped_gun.detect()


def quit_handler(call):
    print("quitting")
    # a normal exit won't work if the program hangs, need to do this
    os.kill(os.getpid(), signal.SIGTERM)


def on_click_handler(x, y, button, pressed):
    # if shooting detected, tell puller we are enabled to kick off pulling down
    if button == mouse.Button.left and pressed:
        puller.enabled = True
    else:
        puller.enabled = False


if __name__ == "__main__":
    print("press L to quit")
    # start our custom pull down listener
    threading.Thread(target=puller.pull_down, args=(False,)).start()

    # enable listening to keyboard and mouse events
    m.hook(mouse_handler)
    keyboard.on_release_key('e', keyboard_handler)
    keyboard.on_release_key('l', quit_handler)
    with mouse.Listener(on_click=on_click_handler) as listener:
        listener.join()
