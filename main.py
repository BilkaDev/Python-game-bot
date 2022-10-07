import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from windowcapture import WindowCapture
from hero import Hero

import time
import keyboard

HEAL_SHORTCUT = '0'
# 2 skill must be +1 key
ATTACK_SHORTCUT = '6'

CD_FIRST_ATTACK_SPELL = 7
HP_MIN = 0.7

wincap = WindowCapture('CABAL')
hero = Hero(CD_FIRST_ATTACK_SPELL)

# press "q" to stop! "e"  to start
is_run = False
while True:
    if is_run:
        is_run = not keyboard.is_pressed('q')
        # loop_time = time.time()
        hp_target_image = wincap.get_hp_target_img()
        # cv2.imshow('Result', fullscreen_image)
        # cv2.waitKey()
        isTarget = hero.is_target(hp_target_image)
        hero.check_hp(hp_target_image, HP_MIN, HEAL_SHORTCUT)
        # print('FPS {}'.format(time.time() - loop_time))
        # loop_time = time.time()

        if isTarget:
            hero.attack(ATTACK_SHORTCUT)
        else:
            hero.stop_attack()
            hero.get_loot()
            hero.check_backpack(wincap)
            hero.find_target()
            time.sleep(0.2)
    else:
        is_run = keyboard.is_pressed('e')
