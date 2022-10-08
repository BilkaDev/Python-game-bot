import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from windowcapture import WindowCapture
from hero import Hero
import config

import time
import keyboard

wincap = WindowCapture(config.game_name)
hero = Hero()

# press "q" to stop! "e"  to start.
is_run = False
while True:
    hero.check_backpack('')
    # if is_run:
    #     is_run = not keyboard.is_pressed('q')
    #     # loop_time = time.time()
    #     hp_target_image = wincap.get_hp_target_img()
    #     # cv2.imshow('Result', fullscreen_image)
    #     # cv2.waitKey()
    #     isTarget = hero.is_target(hp_target_image)
    #     hero.check_hp(hp_target_image)
    #     # print('FPS {}'.format(time.time() - loop_time))
    #     # loop_time = time.time()
    #
    #     if isTarget:
    #         hero.attack()
    #     else:
    #         hero.stop_attack()
    #         hero.get_loot()
    #         hero.check_backpack(wincap)
    #         hero.find_target()
    #         time.sleep(0.2)
    # else:
    #     is_run = keyboard.is_pressed('e')
