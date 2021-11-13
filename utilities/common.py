import os
from datetime import datetime


def get_root_directory():
    return str(os.path.dirname(os.path.abspath(__file__))).replace("utilities", "")


def get_time_stamp():
    return str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))