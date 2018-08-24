import os
import json
import shutil
import filecmp

from Log import Log

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
    log = Log('settings', 'green')
    if SETTINGS is None:
        try:
            log.msg(None, [
                ('loading settings...', 'default')
            ], print=True)
            f = open(DIR, 'r', encoding='utf-8')
            SETTINGS = json.load(f)
            f.close()
            if not filecmp.cmp(DIR, DIR_BACKUP):
                shutil.copyfile(DIR, DIR_BACKUP)
        except Exception as e:
            log.msg('error', [
                ('loading settings...', 'default')
            ], print=True)
            print(RED + str(e) + RESET)
            print(GREEN + '[settings] regenerating settings file...' + RESET)
            f_b = open(DIR_BACKUP, 'r', encoding='utf-8')
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
    f = open(DIR, 'w', encoding='utf-8')
    json.dump(SETTINGS, f, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    shutil.copyfile(DIR, DIR_BACKUP)
    f.close()
