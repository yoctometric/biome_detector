import pydirectinput as pd  # needed for commands such as opening chat
import pyautogui as pg      # used elsewhare due to pydirect being generally unstable
import time
import os, pathlib
from PIL import Image
import argparse
import datetime
import random
import mouse
"""
This script is designed to be run on minecraft version 1.13.1
"""

SCREENSHOT_KEY = 'i'    # key (configured in minecraft settings) which takes a screenshot

ITER_COMPLETED = "FINISHED_ITERATION"
START_TIME = None   # set by main
n_new_files = 0     # number of new files generated in this run

def teleport(range: int, origin: tuple=(0, 0)) -> None:
    """
    Runs the spreadplayers command to teleport the player randomly around origin
    """
    pd.press('t')
    pg.typewrite(f'/spreadplayers {origin[0]} {origin[1]} 0 {range} false @a')
    pd.press('enter')


def run_biome_command() -> None:
    """
    Runs a command to print the player's current biome to chat. 
    Requires the biome-detector datapack by TheRedEngineer to be installed and set up:
        - http://www.theredengineer.com/biome-detector.html
    """

    # of note is that this will return an integer from the 'old' biome ids.
    # https://minecraft.fandom.com/wiki/Biome/IDs_before_1.13
    pd.press('t')
    pg.write('/scoreboard players get @p playerBiome')
    pd.press('enter')


def follow(file, sleep_sec=0.2):
    """
    Yield each line from a file as they are written.
    `sleep_sec` is the time to sleep after empty reads. 

    source: https://stackoverflow.com/questions/12523044/how-can-i-tail-a-log-file-in-python
    """
    # do an initial readlines to skip the first batch
    file.readlines()

    line = ''
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        else:
            time.sleep(sleep_sec)


def get_new_data(range: int, load_wait: int):
    """
    Teleports the player, takes a screenshot, and saves it with the biome name
    """
    teleport(range)

    # wait for world to load
    time.sleep(load_wait)

    # then grab the biome and screenie
    run_biome_command()
    time.sleep(0.1)
    take_screenshots(6)
    time.sleep(1)

    # indicate that data collection iteration has finished
    pd.press('t')
    pg.write(ITER_COMPLETED)
    pd.press('enter')


def take_screenshots(n: int):
    """
    Takes n screenshots at random rotations around the player in minecraft and names it with the biome_type command
    requires screenshot key to be set to SCREENSHOT_KEY
    """
    for _ in range(n):
        time.sleep(1)
        pd.press(SCREENSHOT_KEY)
        time.sleep(0.1)
        mouse._os_mouse.move_relative(random.randrange(100, 1000) ,0)


def modify_screenshot(fname, screenshots_dir, data_dir, biome_id):
    """
    Renames the screenshot at fname to biome_id, and scales it as well
    """
    img_path = pathlib.Path(screenshots_dir, fname)
    assert img_path.exists(), f"Image path {img_path} DNE"
    
    # resize the image and convert to jpeg
    scale = 2
    with Image.open(img_path) as im:
        (width, height) = (im.width // scale, im.height // scale)
        im_resized = im.resize((width, height))
        im_resized = im_resized.convert('RGB')  # JPEG cant handle RGBA

        save_image(im_resized, data_dir, biome_id)
    
    os.remove(img_path)
    assert not img_path.exists()


def save_image(im, data_dir, biome_id):
    """
    Saves an image at a unique name path
    """
    global n_new_files # TODO: awful. I hate it
    n_new_files += 1

    dir = pathlib.Path(data_dir, f'biome_{biome_id}')
    dir.mkdir(parents=True, exist_ok=True)
    num_files = len(list(dir.glob('*')))
    fpath = pathlib.Path(dir, f'biome_{biome_id}_{num_files}.jpg')
    im.save(fpath)

    # print("Saved resized image at ", fpath)


def line_recieved(line: str, last_biome_id, last_screenshot_names, args):
    """
    Performs an action based on the contents of <line> whenever it recierves a new one from the log file
    """
    screenshot_name = 'none'
    biome_id = -1
    reset = False

    if '[CHAT]' in line:
        # handle starting the bot
        if line.endswith("start\n"):
            print("starting!")
            get_new_data(args.tele_range, args.load_delay)

        if '[playerBiome]' in line:
            # store the biome index integer
            biome_id = int(line.split(" ")[-2])
            # print("Biome id:", biome_id)

        if 'Saved screenshot as' in line:
            # store the name of the file
            screenshot_name = line.split(" ")[-1].replace('\n', '')
            # print("A screenshot was saved as ", screenshot_name)

        # handle recieving news that a data collection iteration has finished
        if ITER_COMPLETED in line:
            # print("now modifying screenshots based on ", last_screenshot_names)

            for screenie in last_screenshot_names:
                modify_screenshot(screenie, args.screenshots_dir, args.data_dir, last_biome_id)

            print(f"Teleporting. Uptime: {datetime.datetime.now() - START_TIME}.    Total new files: {n_new_files}")

            get_new_data(args.tele_range, args.load_delay)
            reset = True    # reset vars
    
    return biome_id, screenshot_name, reset


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="screenbot: A script which automatically gathers screenshots of a minecraft world at random locations and labels them with the biome id of the location the screenshot was taken from.",
        epilog=r"Example: py .\screenbot.py C:\Users\zande\AppData\Roaming\.minecraft\1.13.1Install\screenshots C:\Users\zande\Documents\Classes\F2022\ECE491\scraping\data C:\Users\zande\AppData\Roaming\.minecraft\1.13.1Install\logs\latest.log 120 15 99999"
        )
    
    parser.add_argument('screenshots_dir', type=pathlib.Path, help="The path to the directory where minecraft saves its screenshots. Usually found in .minecraft/screenshots/")
    parser.add_argument('data_dir', type=pathlib.Path, help="The root directory where data is to be saved.")
    parser.add_argument('latest_log', type=pathlib.Path, help="The full path to the 'latest.log' file for minecraft. Often found in .minecraft/logs/latest.log")
    parser.add_argument('runtime', type=int, help="Amount of minutes to (roughly) run the program for.")
    parser.add_argument('load_delay', type=int, help="Number of seconds to wait after teleporting for the world to load (recommend 10-15)")
    parser.add_argument('tele_range', type=int, help="Range to teleport around in")

    args = parser.parse_args()
    START_TIME = datetime.datetime.now()
    stop_time = START_TIME + datetime.timedelta(minutes=args.runtime)

    # ensure relevant paths exist
    log_path = args.latest_log
    assert log_path.exists()
    screenshots_dir = args.screenshots_dir
    assert screenshots_dir.exists()
    data_dir = args.data_dir
    assert data_dir.exists()

    # before reading from the log file, add a dummy to the end of it so that we don't accidentally start
    with open(log_path, 'a') as file:
        file.write("began running screenbot\n")

    # open the log file and read it
    with open(log_path, 'r') as file:
        last_biome_id = -1
        last_screenshot_names = []

        # set the time at which the bot should notice it has fallen asleep and needs to kick back into gear
        alarm_time = datetime.datetime.now() + datetime.timedelta(seconds=int(args.load_delay*2.5))

        for line in follow(file):
            lbi, lsn, reset = line_recieved(line, last_biome_id, last_screenshot_names, args)

            # if a valid biome id is recieved, update it
            if lbi != -1:
                last_biome_id = lbi

            # if a valid file name is recieved, add it
            if lsn != "none":
                last_screenshot_names.append(lsn)

            # finally, if a reset was called wipe all that
            if reset:
                last_biome_id = 0
                last_screenshot_names = []

                # update alarm time so that the alarm doesn't go off accidentally
                alarm_time = datetime.datetime.now() + datetime.timedelta(seconds=int(args.load_delay*2.5))

            # If nothing has happened for a while, resend ITER_COMPLETED
            if datetime.datetime.now() > alarm_time:
                print("Bot has fallen still for too long. Wake up!")
                alarm_time = datetime.datetime.now() + datetime.timedelta(seconds=int(args.load_delay*2.5))

                # indicate that data collection iteration has finished (again)
                time.sleep(0.1)
                pd.press('t')
                pg.write(ITER_COMPLETED)
                pd.press('enter')

            # complete execution if time has run out
            if datetime.datetime.now() > stop_time:
                exit(0)
            