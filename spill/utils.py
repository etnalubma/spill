import os
import sys
from subprocess import call


def get_uptime():
    try:
        f = open("/proc/uptime")
        contents = f.read().split()
        f.close()
    except:
        return None

    total_seconds = float(contents[0])

    # Helper vars:
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    # Get the days, hours, etc:
    days = int(total_seconds / DAY)
    hours = int((total_seconds % DAY) / HOUR)
    minutes = int((total_seconds % HOUR) / MINUTE)
    seconds = int(total_seconds % MINUTE)

    string = "%d %s, %d:%d:%d" % (days,
                    days > 1 and 'days' or 'day', hours, minutes, seconds)

    return string


def get_editor():
    """Return a sequence of possible editor binaries for the current platform"""
    # kindly taken from bzr

    for varname in 'VISUAL', 'EDITOR':
        if varname in os.environ:
            yield os.environ[varname], '$' + varname

    if sys.platform == 'win32':
        for editor in 'wordpad.exe', 'notepad.exe':
            yield editor, None
    else:
        for editor in ['/usr/bin/editor', 'vi', 'pico', 'nano', 'joe']:
            yield editor, None


def run_editor(filename):
    """Try to execute an editor to edit the commit message."""
    # kindly taken from bzr
    for candidate, candidate_source in get_editor():
        edargs = candidate.split(' ')
        try:
            ## mutter("trying editor: %r", (edargs +[filename]))
            x = call(edargs + [filename])

        except OSError, e:
            if candidate_source is not None:
                # We tried this editor because some user configuration (an
                # environment variable or config file) said to try it.  Let
                # the user know their configuration is broken.
                trace.warning(
                    'Could not start editor "%s" (specified by %s): %s\n'
                    % (candidate, candidate_source, str(e)))
            continue
            raise

        if x == 0:
            return open(filename).read()
        elif x == 127:
            continue
        else:
            break
    print """Could not start any editor."""
