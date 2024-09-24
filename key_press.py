import pyautogui
import keyboard
import time


key_cords = {
    "A": [(120, 925)], "Ф": [(120, 925)], "4": [(120, 925)],
    "S": [(220, 925)], "І": [(220, 925)], "Ы": [(220, 925)], "5": [(220, 925)],
    "D": [(360, 925)], "В": [(360, 925)], "6": [(360, 925)],
    "W": [(120, 882)], "Ц": [(120, 882)], "8": [(120, 882)],
    "Q": [(150, 500), (1050, 1048)], "Й": [(150, 500), (1050, 1048)], "7": [(150, 500), (1050, 1048)],
}

def click_on_cords(key):
    if key == '1':
        pyautogui.hotkey('esc')
    if key in key_cords:
        pyautogui.hotkey('backspace', 'backspace')
        cords = key_cords[key]
        for cord in cords:
            pyautogui.click(cord)
            if len(cords) > 1:
                time.sleep(0.2)

def on_key_press(event):
    click_on_cords(event.name)

def start_keys():
    keyboard.on_press(on_key_press)

def stop_keys():
    keyboard.unhook_all()
