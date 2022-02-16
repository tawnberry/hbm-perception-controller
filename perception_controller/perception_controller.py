import os
from python_imagesearch.imagesearch import click_image, imagesearch
from win32gui import GetWindowText, GetForegroundWindow
import pyperclip
import pyautogui
import time


"""
1. Prompt User = SETUP
2. Setup Perception = SETUP
3. Start recording
4. Wait for trigger
5. Stop recording
6. Export file
7. Rename next recording

Go back to step 3 if we have not reached the index amount.

need a time out feature?

"""
IMAGE_SEARCH_TIME = 30              # 30 seconds
TRIGGER_SEARCH_TIME = 60 * 30       # 30 minutes
PERCEPTION_APP = 'perception'

PERCEPTION_BUTTONS = {
    'start': 'start_button.png',
    'stop': 'stop_button.png',
    'file': 'file_button.png',
    'ok': 'export_ok_button.png',
    'perception_icon': 'perception_icon.png',
    'naming': 'naming_button.png',
    'export_active': 'exporting_active.png',
    'export': 'export_button.png',
    'naming_num': 'naming_serial_number.png',
    'naming_ok': 'naming_ok_button.png',
}

TRIGGERS = {
    '5': '5.png', '6': '6.png', '7': '7.png', '8': '8.png', '9': '9.png', '10': '10.png',
    '11': '11.png', '12': '12.png', '13': '13.png', '14': '14.png', '15': '15.png', '16': '16.png',
    '17': '17.png', '18': '18.png', '19': '19.png', '20': '20.png', '21': '21.png', '22': '22.png',
    '23': '23.png', '24': '24.png', '25': '25.png', '26': '26.png', '27': '27.png', '28': '28.png',
    '29': '29.png', '30': '30.png', '31': '31.png', '32': '32.png', '33': '33.png', '34': '34.png',
    '35': '35.png', '36': '36.png', '37': '37.png', '38': '38.png', '39': '39.png', '40': '40.png',
    '41': '41.png', '42': '42.png', '43': '43.png', '44': '44.png', '45': '45.png', '46': '46.png',
    '47': '47.png', '48': '48.png', '49': '49.png', '50': '50.png',
}


def set_up_files(perception_dir, trigger_dir):
    for perception_button in PERCEPTION_BUTTONS.keys():
        PERCEPTION_BUTTONS[perception_button] = os.path.join(perception_dir, PERCEPTION_BUTTONS[perception_button])

    for trigger_button in TRIGGERS.keys():
        TRIGGERS[trigger_button] = os.path.join(trigger_dir, TRIGGERS[trigger_button])


def get_active_window():
    return GetWindowText(GetForegroundWindow()).lower()


def make_perception_active():
    while PERCEPTION_APP not in get_active_window():
        click_on_image(PERCEPTION_BUTTONS['perception_icon'])


def look_for_image(image, timeout=IMAGE_SEARCH_TIME):
    """
    This will return True if it found the inputted image is found.
    The timeout decorator will throw an exception if it can't find the image.

    :return:
    """
    try:
        current_time = time.process_time()
        im = None
        while im is None:
            im = pyautogui.locateOnScreen(image)
            time.sleep(0.5)
            if time.process_time() - current_time > timeout:
                return False

        return True

    except FileNotFoundError as err:
        print(err)
        return False


def click_on_image(image, timeout=IMAGE_SEARCH_TIME, button='left'):
    try:
        current_time = time.process_time()

        pos = imagesearch(image)
        while pos[0] == -1:
            pos = imagesearch(image)
            time.sleep(0.5)

            if time.process_time() - current_time > timeout:
                raise False

        click_image(image, pos, button, 0.1)

        return True

    except FileNotFoundError as err:
        print(err)
        return False


def start_record():
    print("Start Recording...")
    click_on_image(PERCEPTION_BUTTONS['start'])


def stop_record():
    print("Stop Recording...")
    click_on_image(PERCEPTION_BUTTONS['stop'])


def wait_for_trigger(trigger_num):
    print(f"Waiting for trigger {trigger_num}")
    look_for_image(TRIGGERS[trigger_num])


def export_file():
    """
    Do the exporting sequence steps:
    1. Find File and left click to bring up the pop-out menu
    2. Find Export Recording... button and left click it. This will bring up the exporting menu
        Note: The export window is assumped to be setup the way you want before we export.
    3. In the exporting menu, find the Ok button. Left click it.
    3. In the exporting menu, find the Ok button. Left click it.
    4. A exporting process window comes up. Wait for this to complete before we continue.
    """
    # This is the sequence on how to we export.
    if click_on_image(PERCEPTION_BUTTONS['file']):
        print("Go to File")
        # We found the file selection so we go to the export button
        if click_on_image(PERCEPTION_BUTTONS['export']):
            print("Go to Export")
            # Once we find the export selection, we can move to the OK for the export window
            if click_on_image(PERCEPTION_BUTTONS['ok']):
                print("Clicked OK")
                # While Perception is exporting, a window pops up to show it's process. We check for this window.
                print("checking for export pop up \n")
                if look_for_image(PERCEPTION_BUTTONS['export_active']):
                    # Once the exporting process window is up,
                    # we must wait for it to complete and go away before continuing.
                    while look_for_image(PERCEPTION_BUTTONS['export_active'], timeout=1):
                        export_msg = "Waiting for export to complete"
                        print(export_msg, end="")
                        print('\b' * (len(export_msg) + 1), end="", flush=True)
                        time.sleep(0.5)

                else:
                    raise Exception(f"Cannot find {PERCEPTION_BUTTONS['export_active']}")
            else:
                raise Exception(f"Cannot find {PERCEPTION_BUTTONS['ok']}")
        else:
            raise Exception(f"Cannot find {PERCEPTION_BUTTONS['export']}")
    else:
        raise Exception(f"Cannot find {PERCEPTION_BUTTONS['file']}")


def change_recording_name(file_index):
    if click_on_image(PERCEPTION_BUTTONS['naming']):
        # We copy the name to the clip board to keep the naming format
        current_file_name = copy_to_clipboard()
        pyautogui.typewrite(update_recording_name(current_file_name, file_index))
        if click_on_image(PERCEPTION_BUTTONS['naming_num']):
            select_all()
            pyautogui.typewrite('1')

            if click_on_image(PERCEPTION_BUTTONS['naming_ok']) is False:
                raise Exception(f"Cannot find {PERCEPTION_BUTTONS['naming_ok']}")

        else:
            raise Exception(f"Cannot find {PERCEPTION_BUTTONS['naming_num']}")

    else:
        raise Exception(f"Cannot find {PERCEPTION_BUTTONS['naming']}")


def copy_to_clipboard():
    # This prevents last copy replacing current copy of null.
    pyperclip.copy("")
    pyautogui.hotkey('ctrl', 'c')

    # ctrl-c is usually very fast but your program may execute faster
    time.sleep(.01)

    return pyperclip.paste()


def select_all():
    pyautogui.hotkey('ctrl', 'a')


def update_recording_name(file_name, index):
    current_index = str(index) + "N"
    print(current_index)
    next_index = str(index + 1) + "N"
    print(next_index)
    new_file_name = file_name.replace(current_index, next_index)

    return new_file_name





