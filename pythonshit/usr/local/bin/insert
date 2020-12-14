#!/usr/bin/env python3
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import sys


f=''
usekey=''
autoenter=False

def on_press(key):
    global usekey
    if key == Key.esc:
        f.close()
        return False  # stop listener
    if usekey=='':
        usekey=key
        print('Will use: '+str(usekey))
    elif key==usekey:
        print('UseKey pressed: ' + str(key))
        line = f.readline()
        if not line:
            print('Reached EOF')
            f.close()
            return False
        else:
            pyperclip.copy(line.strip())
            print(pyperclip.paste())
            
            try:
                keyboardController = Controller()
                keyboardController.press(Key.ctrl.value)
                keyboardController.press('v')
                keyboardController.release('v')
                keyboardController.release(Key.ctrl.value)
                if autoenter:
                    keyboardController.press(Key.enter.value)
                    keyboardController.release(Key.enter.value)
            except:
                print('failed to press crtl-v')


def main(filename, enter: ('makes an enter after insert', 'flag', 'e')):
    "Insert line by line of a file into a GUI by just pressing a key"
    global f
    global autoenter
    autoenter=enter
    f=open(filename,"r")
    print('Define the Key to use by pressing it:')
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys


if __name__ == '__main__':
    import plac; plac.call(main)

