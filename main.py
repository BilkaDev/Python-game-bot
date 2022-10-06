from windowcapture import WindowCapture
from hero import Hero

import time
import pyautogui
import pydirectinput
import keyboard
import cv2

HEAL_SHORTCUT = '0'
# 2 skill must be +1 key
ATTACK_SHORTCUT = '6'

CD_FIRST_ATTACK_SPELL = 4.5
HP_MIN = 0.7

wincap = WindowCapture('CABAL')
hero = Hero(CD_FIRST_ATTACK_SPELL)
# click cabal desktop
pyautogui.click(485, 150)
pydirectinput.keyDown("z")
time.sleep(0.2)
pydirectinput.keyUp("z")

# press "q" to stop!
while not keyboard.is_pressed('q'):
    loop_time = time.time()
    hp_target_image = wincap.get_hp_target_img()
    # cv2.imshow('Result', fullscreen_image)
    # cv2.waitKey()
    isTarget = hero.is_target(hp_target_image)

    hero.check_hp(hp_target_image, HP_MIN, HEAL_SHORTCUT)
    print('FPS {}'.format(time.time() - loop_time))
    loop_time = time.time()

    if isTarget:
        hero.attack(ATTACK_SHORTCUT)
    else:
        hero.stop_attack()
        hero.get_loot()
        hero.find_target()
        time.sleep(0.2)
