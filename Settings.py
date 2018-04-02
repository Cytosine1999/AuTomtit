import os
import json
import shutil
import filecmp

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

DIR, _ = os.path.split(os.path.realpath(__file__))
DIR_BACKUP = DIR + '/.settings_backup.json'
DIR += '/settings.json'

SETTINGS = None
FLAG = False


def load():
    global SETTINGS
    if SETTINGS is None:
        try:
            print(GREEN + '[settings] loading settings...' + RESET)
            f = open(DIR, 'r')
            SETTINGS = json.load(f)
            f.close()
            if not filecmp.cmp(DIR, DIR_BACKUP):
                shutil.copyfile(DIR, DIR_BACKUP)
        except Exception as e:
            print(RED + str(e) + RESET)
            print(GREEN + '[settings] regenerating settings file...' + RESET)
            f_b = open(DIR_BACKUP, 'r')
            SETTINGS = json.load(f_b)
            f_b.close()
            shutil.copyfile(DIR_BACKUP, DIR)
    return SETTINGS


def dump(profile):
    global SETTINGS, FLAG
    SETTINGS = profile
    FLAG = True


def flush():
    global SETTINGS
    if SETTINGS is None or not FLAG:
        return
    print(GREEN + '[settings] saving settings...' + RESET)
    f = open(DIR, 'w')
    json.dump(SETTINGS, f, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    shutil.copyfile(DIR, DIR_BACKUP)
    f.close()
