# Desktop stand-in for TI's ti_system module (tests only).
# get_key() returns the next key from KEYS; when the list is used up it
# raises KeyboardInterrupt, which ends the graphical mode.
KEYS = []
HOOK = []       # functions run once, at the first get_key (tests use it)


def get_key(wait=0):
    while HOOK:
        HOOK.pop(0)()
    if KEYS:
        return KEYS.pop(0)
    raise KeyboardInterrupt()
