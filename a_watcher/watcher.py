import pyautogui


class Watcher:

    def __init__(self):
        self.folder = 'a_watcher'

    def get_screen(self):
        screenshot_name = self.folder + '/screenshot.png'
        screenshot = pyautogui.screenshot(screenshot_name)
        return screenshot
