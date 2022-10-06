from windowcapture import WindowCapture
from hero import Hero

import time
import pyautogui
import pydirectinput
import keyboard

HEAL_SHORTCUT = '0'

# 2 skill must be +1 key
ATTACK_SHORTCUT = '6'

CD_FIRST_ATTACK_SPELL = 4.5

wincap = WindowCapture('CABAL')
hero = Hero(CD_FIRST_ATTACK_SPELL)
# click cabal desktop
pyautogui.click(485, 150)
pydirectinput.keyDown("z")
time.sleep(0.2)
pydirectinput.keyUp("z")

# press "q" to stop!
while not keyboard.is_pressed('q'):
    # loop_time = time.time()
    fullscreen_image = wincap.get_screenshot()
    isTarget = hero.is_target(fullscreen_image)

    hero.check_hp(fullscreen_image, HEAL_SHORTCUT)
    # print('FPS {}'.format(time.time() - loop_time))
    # loop_time = time.time()

    if isTarget:
        hero.attack(ATTACK_SHORTCUT)
    else:
        hero.stop_attack()
        hero.get_loot()
        hero.find_target()
        time.sleep(0.2)
