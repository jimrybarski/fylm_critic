import logging
import argparse

# Show us all log messages in the terminal as the program runs
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# If any errors occur, write those log messages to a file in addition to showing them on the screen
# We're doing this since Jim keeps accidentally closing the terminal and losing important debug information
error_handler = logging.FileHandler("/var/log/fylm_error.log")
error_handler.setLevel(logging.ERROR)

debug_handler = logging.FileHandler("/var/log/fylm.log")
debug_handler.setLevel(logging.DEBUG)

# Actually instantiate the logger
log = logging.getLogger()
log.addHandler(stream_handler)
log.addHandler(error_handler)
log.addHandler(debug_handler)


class Args(dict):
    """
    This class just allows us to get arguments from argparse using dot syntax.
    """
    pass

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="count", default=0, help="Specify -v through -vvv")
    args = parser.parse_args(namespace=Args())

    # default = ERROR
    # -v = WARN
    # -vv = INFO
    # -vvv = DEBUG
    log_level = 40 - args.v * 10
    log.setLevel(log_level)

except:
    log.exception("Unhandled exception!")
    log.critical("""
    =========================  Unhandled exception!  =========================

    fylm_critic crashed! Please copy and paste the traceback and
    create a Github issue at https://github.com/jimrybarski/fylm_critic/issues

    Protip: put tracebacks and code inbetween triple backticks (```) to format
    them like code.

    ==========================================================================
    """)
