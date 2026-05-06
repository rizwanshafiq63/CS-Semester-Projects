# server/logger.py
#
# Levels:
#   INFO      = cyan
#   SUCCESS   = green
#   WARNING   = yellow
#   ERROR     = red
#   SECURITY  = magenta (key lifecycle, KDC events)
#   BLOCKCHAIN= blue

import sys
import time


class Color:
    RESET   = "\033[0m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"


class Logger:

    LOG_FILE = "data/logs/server.log"

    @staticmethod
    def _timestamp():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def _write_to_file(text: str):
        try:
            with open(Logger.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception:
            pass  # avoid crashes due to logging errors

    @staticmethod
    def _log(prefix: str, color: str, message: str):
        ts = Logger._timestamp()
        formatted = f"[{ts}] [{prefix}] {message}"
        colored = f"{color}{formatted}{Color.RESET}"

        print(colored)
        Logger._write_to_file(formatted)

    # Logging helper methods

    @staticmethod
    def info(msg: str):
        Logger._log("INFO", Color.CYAN, msg)

    @staticmethod
    def success(msg: str):
        Logger._log("SUCCESS", Color.GREEN, msg)

    @staticmethod
    def warning(msg: str):
        Logger._log("WARNING", Color.YELLOW, msg)

    @staticmethod
    def error(msg: str):
        Logger._log("ERROR", Color.RED, msg)

    @staticmethod
    def security(msg: str):
        Logger._log("SECURITY", Color.MAGENTA, msg)

    @staticmethod
    def blockchain(msg: str):
        Logger._log("BLOCKCHAIN", Color.BLUE, msg)
