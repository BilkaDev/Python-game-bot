import win32gui, win32con, win32api

import time


def get_pixel(window, x, y):
    wDC = win32gui.GetWindowDC(window)
    return win32gui.GetPixel(wDC, x, y)


def mouse_click(pos):
    x, y = pos
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

