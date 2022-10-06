import win32gui, win32api
import time


def get_pixel(window):
    wDC = win32gui.GetWindowDC(window)
    x, y = win32gui.GetCursorPos()
    print(x, y)
    print(win32gui.GetPixel(wDC, x, y))
    print(rgbint2rgbtuple(win32gui.GetPixel(wDC, x, y)))
    time.sleep(1)


def set_cursor_pos(x, y):
    win32api.SetCursorPos(x, y)


def rgbint2rgbtuple(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return (red, green, blue)
