import win32gui


def get_pixel(window, x, y):
    wDC = win32gui.GetWindowDC(window)
    return win32gui.GetPixel(wDC, x, y)
