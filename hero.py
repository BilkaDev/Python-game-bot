from vision import Vision

# import pytesseract
import pydirectinput
import time


# import cv2

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\royal\AppData\Local\Tesseract-OCR\tesseract.exe'


class Hero:
    # properties
    is_heal = False
    target_img = Vision('image/target-monster-icon.jpg')
    is_attack = False
    cd = 0.
    last_time_cast_spell = time.time()

    def __init__(self, cd):
        self.cd = cd

    def check_hp(self, img, shortcut):
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

        # NIE ZMIENIAC BO NA VM SĄ INNE WARTOŚĆI
        y = 14
        x = 75
        h = 12
        w = 130
        crop = img[y:y + h, x:x + w]
        b, g, r = crop[6, 91]
        if 150 > r:
            self.is_heal = True
            self.heal(shortcut)
        else:
            self.is_heal = False

    def heal(self, shortcut):
        pydirectinput.keyDown(shortcut)
        time.sleep(0.1)
        pydirectinput.keyUp(shortcut)

    def is_target(self, screen_to_search):
        # NIE ZMIENIAC BO NA VM SĄ INNE WARTOŚĆI
        y = 0
        x = 345
        h = 40
        w = 40
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
