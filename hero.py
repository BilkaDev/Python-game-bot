from vision import Vision
import config
import utils

# import pytesseract
import pydirectinput
import time


# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\royal\AppData\Local\Tesseract-OCR\tesseract.exe'


class Hero:
    # properties
    target_img = Vision('image/target-monster-icon.jpg')
    is_heal = False
    is_attack = False
    is_full_backpack = False
    cd = 0.
    last_time_cast_spell = time.time()
    time_last_check_bp = time.time()

    def __init__(self, cd):
        self.cd = cd

    def check_hp(self, img, hp, shortcut):
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
            self.heal(shortcut)
        else:
            self.is_heal = False

    def check_backpack(self, wincap):
        if self.time_last_check_bp + 1 > time.time():
            return
        x, y = config.item_bp_last_slot
        utils.mouse_click(x, y)
        lists = config.last_item_in_bp_location
        check = False
        for pos in lists:
            if wincap.get_pixel_onscreen(pos) != 1315602:
                check = True
        self.is_full_backpack = check
        self.time_last_check_bp = time.time()

    def heal(self, shortcut):
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

    def attack(self, attack_shortcut):
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
