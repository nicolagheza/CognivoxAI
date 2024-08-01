import os
from getpass import getpass


class Utils:
    @staticmethod
    def set_env(var: str):
        if not os.environ.get(var):
            os.environ[var] = getpass(f"{var}: ")
