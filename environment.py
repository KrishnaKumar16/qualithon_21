from utilities.web import BrowserDrivers, BrowserUtils
from utilities.logs import Logs
from utilities.common import get_root_directory
import os


def before_scenario(context, scenario):
    Logs()
    context.driver = BrowserDrivers.get_chrome_driver()
    utils = BrowserUtils(context.driver)
    utils.maximizeWindow()


def after_scenario(context, scenario):
    utils = BrowserUtils(context.driver)
    if scenario.status == 'failed':
        utils.capture_screenshot(os.path.join(get_root_directory(), 'temp'))
    utils.closeBrowserWindow()

