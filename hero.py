import cv2

from vision import Vision
import utils
from windowcapture import WindowCapture
import config

import pytesseract
import pydirectinput
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\royal\AppData\Local\Tesseract-OCR\tesseract.exe'


class Hero:
    # properties
    target_img = Vision('image/target-monster-icon.jpg')
    is_heal = False
    is_attack = False
    is_full_backpack = False
    cd = config.auto["CD_FIRST_ATTACK_SPELL"]
    last_time_cast_spell = time.time()
    time_last_check_bp = time.time()

    def check_hp(self, img):
        hp = config.auto["HP_MIN"]
        # y = 16
        # x = 75
        # h = 17
        # w = 74
        # crop = img[y:y + h, x:x + w]
        # # hp_string = pytesseract.image_to_string(crop, config='digits')
        # hp_string = reader.readtext(gray_img, detail=0)
        # try:
        #     hp_number = int(hp_string)
        #     self.hp = hp_number
        # except:
        #     hp_number = 10
        #     self.hp = hp_number
        y, x, h, w = config.localization_hp_bar
        crop = img[y:y + h, x:x + w]
        b, g, r = crop[int(h / 2), int(w * hp)]
        if 150 > r:
            self.is_heal = True
            self.heal()
        else:
            self.is_heal = False

    def check_backpack(self, wincap):
        img = wincap.get_snip_snap_img(810, 610, 200, 80)
        # cv2.imshow("R", img)
        # cv2.waitKey()
        string = pytesseract.image_to_string(img, config=r'--oem 3 --psm 6')
        self.is_full_backpack = 'cannot gain more items' in string
        if self.time_last_check_bp + 15 > time.time():
            return
        self.time_last_check_bp = time.time()
        if self.is_full_backpack:
            self.item_extract(2)
            self.item_extract(2)

        # old version
        # utils.mouse_click(config.item_bp_last_slot)
        # time.sleep(0.1)
        # lists = config.last_item_in_bp_location
        # check = False
        # for pos in lists:
        #     if wincap.get_pixel_onscreen(pos) != 1315602:
        #         check = True
        # self.is_full_backpack = check
        # self.time_last_check_bp = time.time()
        # if self.is_full_backpack:
        # self.item_extract()

    def item_extract(self, part=2):
        # open inventory
        pydirectinput.press('i')
        time.sleep(0.5)
        # sort items
        sort_x, sort_y = config.extract_localization
        utils.mouse_click([sort_x - 50, sort_y + 30])
        time.sleep(0.8)
        # open slot 1 in inventory
        slot_2_x, slot_2_y = config.item_bp_last_slot
        utils.mouse_click([slot_2_x - 50, slot_2_y])
        time.sleep(0.2)

        inventory_x, inventory_y, inventory_w, inventory_h = config.inventory_box
        count_slot_h, count_slot_v = config.count_slot_hv
        # img = wincap.get_snip_snap_img(730, 165, inventory_w, inventory_h)

        # Open extract item
        utils.mouse_click(config.extract_localization)
        time.sleep(0.3)

        # Select items
        slot_x = (inventory_w / count_slot_h)
        slot_y = (inventory_h / count_slot_v)
        wincap = WindowCapture(config.game_name)
        for y in range(int(count_slot_v / part)):
            self.check_hp(wincap.get_hp_target_img())
            for x in range(count_slot_h):
                point_y = slot_y / 2 + (slot_y * y) + inventory_y
                point_x = slot_x / 2 + (slot_x * x) + inventory_x
                utils.mouse_click([int(point_x), int(point_y)])
                time.sleep(0.2)

        # Agree extract
        utils.mouse_click(config.extract_start_button_localization)
        time.sleep(0.1)
        utils.mouse_click(config.extract_confirm_button_localization)
        time.sleep(0.1)

        # Extracting...
        self.time_sleep_heal(10)

        # Exit
        utils.mouse_click(config.extract_exit_button_localization)
        utils.mouse_click([sort_x - 50, sort_y + 30])
        pydirectinput.press('i')
        time.sleep(0.1)

    def time_sleep_heal(self, s):
        sleep_time = time.time() + s
        wincap = WindowCapture(config.game_name)
        while sleep_time > time.time():
            hp_target_image = wincap.get_hp_target_img()
            self.check_hp(hp_target_image)
            if self.is_heal:
                # hp potion localization
                utils.mouse_click([638, 701])
            time.sleep(0.35)

    def heal(self):
        shortcut = config.shortcuts["HEAL_SHORTCUT"]
        pydirectinput.keyDown(shortcut)
        time.sleep(0.1)
        pydirectinput.keyUp(shortcut)

    def is_target(self, screen_to_search):
        y, x, h, w = config.localization_attack_target
        img = screen_to_search[y:y + h, x:x + w]
        # cv2.imshow('Result', img)
        # cv2.waitKey()
        is_target = self.target_img.is_on_screen(img)
        return is_target

    def attack(self):
        attack_shortcut = config.shortcuts["ATTACK_SHORTCUT"]
        spell_cd_time = self.last_time_cast_spell + self.cd
        if self.is_attack and spell_cd_time > time.time():
            return
        if spell_cd_time > time.time():
            attack_shortcut = str(int(attack_shortcut) + 1)
        else:
            self.last_time_cast_spell = time.time()
        pydirectinput.keyDown(attack_shortcut)
        time.sleep(0.1)
        pydirectinput.keyUp(attack_shortcut)
        self.is_attack = True

    def stop_attack(self):
        self.is_attack = False

    def find_target(self):
        pydirectinput.keyDown('z')
        time.sleep(0.1)
        pydirectinput.keyUp('z')
        time.sleep(0.15)

    def get_loot(self):
        pydirectinput.keyDown('space')
        time.sleep(0.1)
        pydirectinput.keyUp('space')
        pydirectinput.keyDown('space')
        time.sleep(0.1)
        pydirectinput.keyUp('space')
