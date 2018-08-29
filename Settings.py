import os
import sys
import json
import shutil
import filecmp


DIR, _ = os.path.split(os.path.realpath(__file__))
DIR_BACKUP = os.path.join(DIR, '.settings_backup.json')
DIR = os.path.join(DIR, 'settings.json')


SETTINGS = None
FLAG = False


def load():
    global SETTINGS
    if SETTINGS is None:
        try:
            print('[settings] loading settings...')
            settings_file = open(DIR, 'r', encoding='utf-8')
            SETTINGS = json.load(settings_file)
            settings_file.close()
            if not filecmp.cmp(DIR, DIR_BACKUP):
                shutil.copyfile(DIR, DIR_BACKUP)
        except Exception as e:
            print('[settings] cannot load settings...')
            sys.stderr.write(str(e))
            print('[settings] regenerating settings file...')
            settings_backup = open(DIR_BACKUP, 'r', encoding='utf-8')
            SETTINGS = json.load(settings_backup)
            settings_backup.close()
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
    print('[settings] saving settings...')
    f = open(DIR, 'w', encoding='utf-8')
    json.dump(SETTINGS, f, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    shutil.copyfile(DIR, DIR_BACKUP)
    f.close()
