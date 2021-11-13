from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By


def xpath(locator: str):
    return (By.XPATH, locator)


def id(locator: str):
    return (By.ID, locator)


def tagName(locator: str):
    return (By.TAG_NAME, locator)


def className(locator: str):
    return (By.CLASS_NAME, locator)


def cssSelector(locator: str):
    return (By.CSS_SELECTOR, locator)


def linkText(locator: str):
    return (By.LINK_TEXT, locator)


def name(locator: str):
    return (By.NAME, locator)


def partialLinkText(locator: str):
    return (By.PARTIAL_LINK_TEXT, locator)


def image(locator: str):
    return (MobileBy.IMAGE, locator)