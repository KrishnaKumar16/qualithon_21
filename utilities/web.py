from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from unittest.case import TestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.by import By
from utilities.logs import Logs
from utilities.common import get_time_stamp
import os


class BrowserDrivers:

    @staticmethod
    def get_chrome_driver(version=None, headless=None, downloadsLocation=None):
        Logs.log_info("Launching chrome browser")
        chromeOptions = Options()
        if downloadsLocation is not None:
            prefs = {"download.default_directory": downloadsLocation}
            chromeOptions.add_experimental_option("prefs", prefs)
        if headless is not None:
            chromeOptions.add_argument("--headless")
        if version is None:
            return webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
        else:
            return webdriver.Chrome(ChromeDriverManager(version).install(), options=chromeOptions)

    @staticmethod
    def get_gecko_driver(version=None):
        Logs.log_info("Launching firefox browser")
        if version is None:
            return webdriver.Chrome(GeckoDriverManager().install())
        else:
            return webdriver.Chrome(GeckoDriverManager(version).install())

    @staticmethod
    def get_ie_driver(version=None):
        Logs.log_info("Launching IE browser")
        if version is None:
            return webdriver.Chrome(IEDriverManager().install())
        else:
            return webdriver.Chrome(IEDriverManager(version).install())

    @staticmethod
    def get_edge_driver(version=None):
        Logs.log_info("Launching ms edge browser")
        if version is None:
            return webdriver.Chrome(EdgeChromiumDriverManager().install())
        else:
            return webdriver.Chrome(EdgeChromiumDriverManager(version).install())


class BrowserUtils:
    __WebLocator = Tuple[str, str]

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    def switch_to_default(self):
        self.__driver.switch_to.default_content()

    def switch_to_iframe_using_index(self, index: int, wait=0):
        if wait != 0:
            WebDriverWait(self.__driver, wait).until(
                EC.presence_of_all_elements_located((By.XPATH, "//iframe|//frame")))
        self.switch_to_iframe(self.__driver.find_elements(By.XPATH, "//iframe|//frame")[index])
        return self

    def switch_to_iframe(self, frame, wait=0):
        if wait == 0:
            WebDriverWait(self.__driver, wait).until(EC.frame_to_be_available_and_switch_to_it(frame))
        else:
            self.__driver.switch_to.frame(frame)
        return self

    def check_if_iframe_is_present(self):
        try:
            if self.__driver.find_elements(By.TAG_NAME, "iframe") is not []:
                return True
            else:
                return False
        except:
            return False

    def wait_until_iframe_is_loaded(self, frame, wait=20):
        WebDriverWait(self.__driver, wait).until(EC.frame_to_be_available_and_switch_to_it(frame))
        return self

    def switch_to_parent_frame(self):
        self.__driver.switch_to.parent_frame()
        return self

    def switch_to_default(self):
        self.__driver.switch_to.default_content()

    def get_window_handles(self):
        return self.__driver.window_handles

    def switch_to_window(self, window):
        self.__driver.switch_to.window(window)
        return self

    def switch_to_window_based_on_page_title(self, title):
        for window in self.get_window_handles():
            self.switch_to_window(window)
            if title is self.__driver.title or title in self.__driver.title:
                break
            else:
                continue
        return self

    def wait_until_alert_is_displayed(self, wait=20):
        WebDriverWait(self.__driver, wait).until(EC.alert_is_present)
        return self

    def accept_alert(self, wait=20):
        if wait != 0:
            self.wait_until_alert_is_displayed(wait)
        self.__driver.switch_to.alert.accept()
        self.switch_to_default()
        return self

    def dismiss_alert(self, wait=20):
        if wait != 0:
            self.wait_until_alert_is_displayed(wait)
        self.__driver.switch_to.alert.dismiss()
        self.switch_to_default()
        return self

    def fill_text_in_alert(self, text, wait=20):
        if wait != 0:
            self.wait_until_alert_is_displayed(wait)
        self.__driver.switch_to.alert.send_keys(text)
        self.switch_to_default()
        return self

    def get_text_from_alert(self, wait=20):
        if wait != 0:
            self.wait_until_alert_is_displayed(wait)
        alertContent = self.__driver.switch_to.alert.text
        self.switch_to_default()
        return alertContent

    def get_window_load_state(self):
        return self.__driver.execute_script("return document.readyState")

    def is_page_fully_loaded(self):
        if self.get_window_load_state() == 'complete':
            return True
        else:
            return False

    def wait_until_page_is_fully_loaded(self, wait=20):
        i = 0
        while self.is_page_fully_loaded() is False and i < wait:
            sleep(1)
            if self.is_page_fully_loaded() is True:
                break
            else:
                i += 1
                continue
        if self.is_page_fully_loaded() is False:
            raise Exception('Page is still loading even after waiting for ' + str(wait) + ' seconds')
        return self

    def captureScreenshot(self, destination_folder_path):
        Logs.log_info(f"Capturing screenshot and storing it in '{destination_folder_path}'")
        self.__driver.get_screenshot_as_file(destination_folder_path + get_time_stamp() + '.png')
        return self

    def getScreenShotAsBase64(self):
        Logs.log_info("Capturing screenshot as base 64")
        return self.__driver.get_screenshot_as_base64()

    def launchUrl(self, url):
        Logs.log_info(f"Launching url - {url}")
        self.__driver.get(url)

    def openNewTab(self):
        self.__driver.execute_script("window.open('')")

    def minimizeWindow(self):
        Logs.log_info("Minimizing browser window")
        self.__driver.minimize_window()

    def execute_script(self, script, argument=None):
        if argument is None:
            result = self.__driver.execute_script(script)
        else:
            result = self.__driver.execute_script(script, argument)
        return result

    def maximizeWindow(self):
        self.__driver.maximize_window()

    def clearCookies(self):
        self.__driver.delete_all_cookies()

    def closeBrowserTab(self):
        self.__driver.close()

    def closeBrowserWindow(self):
        self.__driver.quit()

    def get_page_title(self):
        Logs.log_info("Fetching page title")
        return self.__driver.title

    def get_current_url(self):
        Logs.log_info("Fetching current url")
        return self.__driver.current_url

    def sleep_for(self, seconds):
        Logs.log_info(f"Sleeping for {seconds} seconds")
        sleep(seconds)
        return self

    def capture_screenshot(self, destination_folder_path):
        self.__driver.get_screenshot_as_file(os.path.join(destination_folder_path, get_time_stamp() + '.png'))
        return self

    def get_screenshot_as_base64(self):
        return self.__driver.get_screenshot_as_base64()

    def get_native_driver(self):
        return self.__driver

    class __BrowserActionDefinitions:
        __WebLocator = Tuple[str, str]

        def __init__(self, locator: __WebLocator, driver: WebDriver):
            self.__locator = locator
            self.__driver = driver

        def select_by_index(self, index):
            Select(self.element_native_action()).select_by_index(index)
            return self

        def select_by_value(self, value):
            Select(self.element_native_action()).select_by_value(value)
            return self

        def select(self):
            Logs.log_info("Selecting element")
            return Select(self.element_native_action())

        def get_test_utils(self):
            return TestCase()

        def execute_script(self, script, argument=None):
            if argument is None:
                self.__driver.execute_script(script)
            else:
                self.__driver.execute_script(script, argument)
            return self

        def element_native_action(self, wait=20):
            Logs.log_info(f"Finding element using locator - {self.__locator}")
            try:
                self.wait_until_element_is_present(wait)
            except:
                pass
            element: WebElement = self.__driver.find_element(self.__locator[0], self.__locator[1])
            return element

        def elements_native_action(self, wait=20):
            try:
                self.wait_until_elements_are_present(wait)
            except:
                pass
            return self.__driver.find_elements(self.__locator[0], self.__locator[1])

        def capture_element_screenshot(self, destination_folder_path):
            screenshot_path = destination_folder_path + get_time_stamp() + '.png'
            Logs.log_info(f"Capturing element screenshot and storing it in path - {screenshot_path}")
            self.element_native_action().screenshot(screenshot_path)
            return self

        def get_element_screenshot_as_base64(self):
            return self.element_native_action().screenshot_as_base64()

        def get_text(self):
            return self.element_native_action().text

        def get_list_of_text_from_elements(self):
            listOfText = []
            for element in self.elements_native_action():
                listOfText.append(element.text)
            return listOfText

        def get_list_of_attributes_from_elements(self, attribute_name):
            listOfText = []
            for element in self.elements_native_action():
                listOfText.append(element.get_attribute(attribute_name))
            return listOfText

        def get_list_of_css_values_from_elements(self, css_property_name):
            listOfText = []
            for element in self.elements_native_action():
                listOfText.append(element.value_of_css_property(css_property_name))
            return listOfText

        def get_attribute(self, attribute_name):
            return self.element_native_action().get_attribute(attribute_name)

        def get_css_property_value(self, css_property):
            return self.element_native_action().value_of_css_property(css_property)

        def validate_element_is_present(self, wait=20):
            self.get_test_utils().assertTrue(self.is_element_present(wait), str(self.__locator) + ' is not present')
            return self

        def validate_element_is_not_present(self, wait=20):
            self.get_test_utils().assertFalse(self.is_element_present(wait), str(self.__locator) + ' is present')
            return self

        def validate_element_is_displayed(self, wait=20):
            self.get_test_utils().assertTrue(self.is_element_displayed(wait), str(self.__locator) + ' is not present')
            return self

        def validate_element_is_not_displayed(self, wait=20):
            self.get_test_utils().assertFalse(self.is_element_displayed(wait), str(self.__locator) + ' is present')
            return self

        def validate_elements_are_present(self, wait=20):
            self.get_test_utils().assertTrue(self.are_elements_present(wait), str(self.__locator) + ' is not present')
            return self

        def validate_elements_are_not_present(self, wait=20):
            self.get_test_utils().assertFalse(self.are_elements_present(wait), str(self.__locator) + ' is present')
            return self

        def validate_list_of_elements_contains_text(self, expected_text):
            for element_text in self.get_list_of_text_from_elements():
                self.get_test_utils().assertIn(element_text, expected_text)
            return self

        def validate_list_of_elements_not_contains_text(self, expected_text):
            for element_text in self.get_list_of_text_from_elements():
                self.get_test_utils().assertNotIn(element_text, expected_text)
            return self

        def validate_list_of_elements_contains_attribute(self, attribute_name, expected_text):
            for element_text in self.get_list_of_attributes_from_elements(attribute_name):
                self.get_test_utils().assertIn(element_text, expected_text)
            return self

        def validate_list_of_elements_not_contains_attribute(self, attribute_name, expected_text):
            for element_text in self.get_list_of_attributes_from_elements(attribute_name):
                self.get_test_utils().assertNotIn(element_text, expected_text)
            return self

        def validate_list_of_elements_contains_css_value(self, css_property, expected_text):
            for element_text in self.get_list_of_css_values_from_elements(css_property):
                self.get_test_utils().assertIn(element_text, expected_text)
            return self

        def validate_list_of_elements_not_contains_css_value(self, css_property, expected_text):
            for element_text in self.get_list_of_css_values_from_elements(css_property):
                self.get_test_utils().assertNotIn(element_text, expected_text)
            return self

        def validate_css_property_value_contains(self, css_property, expected_text):
            self.get_test_utils().assertIn(container=self.get_css_property_value(css_property), member=expected_text)
            return self

        def validate_css_property_value_not_contains(self, css_property, not_expected_text):
            self.get_test_utils().assertNotIn(container=self.get_css_property_value(css_property),
                                              member=not_expected_text)
            return self

        def validate_css_property_value_equals(self, css_property, expected_text):
            self.get_test_utils().assertEqual(self.get_css_property_value(css_property), expected_text)
            return self

        def validate_text_contains(self, expected_text):
            self.get_test_utils().assertIn(container=self.get_text(), member=expected_text)
            return self

        def validate_text_not_contains(self, not_expected_text):
            self.get_test_utils().assertNotIn(container=self.get_text(), member=not_expected_text)
            return self

        def validate_text_equals(self, expected_text):
            self.get_test_utils().assertEqual(self.get_text(), expected_text)
            return self

        def validate_attribute_contains(self, attribute, expected_text):
            self.get_test_utils().assertIn(container=self.get_attribute(attribute), member=expected_text)
            return self

        def validate_attribute_not_contains(self, attribute, not_expected_text):
            self.get_test_utils().assertNotIn(container=self.get_attribute(attribute), member=not_expected_text)
            return self

        def validate_attribute_equals(self, attribute, expected_text):
            self.get_test_utils().assertEqual(self.get_attribute(attribute), expected_text)
            return self

        def wait_until_element_is_present(self, wait=20):
            WebDriverWait(self.__driver, wait).until(EC.presence_of_element_located((self.__locator[0],
                                                                                     self.__locator[1])))
            return self

        def wait_until_element_is_clickable(self, wait=20):
            WebDriverWait(self.__driver, wait).until(EC.element_to_be_clickable((self.__locator[0],
                                                                                 self.__locator[1])))
            return self

        def wait_until_elements_are_present(self, wait=20):
            WebDriverWait(self.__driver, wait).until(EC.presence_of_all_elements_located((self.__locator[0],
                                                                                          self.__locator[1])))
            return self

        def wait_until_element_is_not_displayed(self, wait=20):
            WebDriverWait(self.__driver, wait).until(EC.invisibility_of_element_located((self.__locator[0],
                                                                                         self.__locator[1])))
            return self

        def wait_until_element_is_visible(self, wait=20):
            WebDriverWait(self.__driver, wait).until(EC.visibility_of_element_located((self.__locator[0],
                                                                                       self.__locator[1])))
            return self

        def click(self, wait: int = 20):
            self.element_native_action(wait).click()
            return self

        def clear_text(self, wait: int = 20):
            self.element_native_action(wait).clear()
            return self

        def fill_text(self, text, wait: int = 20):
            self.element_native_action(wait).send_keys(text)
            return self

        def is_element_displayed(self, wait=20):
            if wait != 0:
                self.wait_until_element_is_visible(wait)
            return self.element_native_action().is_displayed()

        def are_elements_present(self, wait=20):
            if wait != 0:
                self.wait_until_elements_are_present(wait)
            if self.elements_native_action() != []:
                return True
            else:
                return False

        def is_element_present(self, wait=20):
            if wait == 0:
                try:
                    self.__driver.find_element(self.__locator[0], self.__locator[1])
                    return True
                except:
                    return False
            else:
                try:
                    self.wait_until_element_is_present(wait)
                    return True
                except:
                    return False

        def scroll_to_element(self):
            self.execute_script("arguments[0].scrollIntoView();", self.element_native_action())
            return self

        def get_action_chains(self):
            return ActionChains(self.__driver)

        def double_lick(self):
            self.get_action_chains().double_click(self.element_native_action()).perform()
            return self

        def drag_and_drop_to_another_element(self, destination_locator: __WebLocator):
            self.get_action_chains().drag_and_drop(source=self.element_native_action(),
                                                   target=self.__driver.find_element(destination_locator[0],
                                                                                     destination_locator[1])).perform()
            return self

        def drag_and_drop_to_destination_offset(self, destination_co_ordinates: Tuple[int, int]):
            self.get_action_chains().drag_and_drop_by_offset(source=self.element_native_action(),
                                                             xoffset=destination_co_ordinates[0],
                                                             yoffset=destination_co_ordinates[1]).perform()
            return self

        def move_to_offset_and_click(self, destination_co_ordinates: Tuple[int, int]):
            self.get_action_chains().move_by_offset(xoffset=destination_co_ordinates[0],
                                                    yoffset=destination_co_ordinates[1]).click().perform()
            return self

        def get_current_window_handle(self):
            return self.__driver.current_window_handle

        def mouse_hover(self):
            Logs.log_info(f"Performing mouse hover using locator - {self.__locator}")
            self.get_action_chains().move_to_element(to_element=self.element_native_action()).perform()

        def __find_keys(self, keys):
            keyboard_keys = dict(NULL='\ue000',
                                 CANCEL='\ue001',  # ^break
                                 HELP='\ue002',
                                 BACKSPACE='\ue003',
                                 BACK_SPACE='\ue003',
                                 TAB='\ue004',
                                 CLEAR='\ue005',
                                 RETURN='\ue006',
                                 ENTER='\ue007',
                                 SHIFT='\ue008',
                                 LEFT_SHIFT='\ue008',
                                 CONTROL='\ue009',
                                 LEFT_CONTROL='\ue009',
                                 ALT='\ue00a',
                                 LEFT_ALT='\ue00a',
                                 PAUSE='\ue00b',
                                 ESCAPE='\ue00c',
                                 SPACE='\ue00d',
                                 PAGE_UP='\ue00e',
                                 PAGE_DOWN='\ue00f',
                                 END='\ue010',
                                 HOME='\ue011',
                                 LEFT='\ue012',
                                 ARROW_LEFT='\ue012',
                                 UP='\ue013',
                                 ARROW_UP='\ue013',
                                 RIGHT='\ue014',
                                 ARROW_RIGHT='\ue014',
                                 DOWN='\ue015',
                                 ARROW_DOWN='\ue015',
                                 INSERT='\ue016',
                                 DELETE='\ue017',
                                 SEMICOLON='\ue018',
                                 EQUALS='\ue019',
                                 NUMPAD0='\ue01a',  # number pad keys
                                 NUMPAD1='\ue01b',
                                 NUMPAD2='\ue01c',
                                 NUMPAD3='\ue01d',
                                 NUMPAD4='\ue01e',
                                 NUMPAD5='\ue01f',
                                 NUMPAD6='\ue020',
                                 NUMPAD7='\ue021',
                                 NUMPAD8='\ue022',
                                 NUMPAD9='\ue023',
                                 MULTIPLY='\ue024',
                                 ADD='\ue025',
                                 SEPARATOR='\ue026',
                                 SUBTRACT='\ue027',
                                 DECIMAL='\ue028',
                                 DIVIDE='\ue029',
                                 F1='\ue031',  # function  keys
                                 F2='\ue032',
                                 F3='\ue033',
                                 F4='\ue034',
                                 F5='\ue035',
                                 F6='\ue036',
                                 F7='\ue037',
                                 F8='\ue038',
                                 F9='\ue039',
                                 F10='\ue03a',
                                 F11='\ue03b',
                                 F12='\ue03c',
                                 META='\ue03d',
                                 COMMAND='\ue03d')
            values = []
            for key in keys:
                for k, v in keyboard_keys.items():
                    if v == key:
                        values.append(k)
            return values

        def press_keys(self, *keys):
            Logs.log_info(f'Pressing keys "{keys}"')
            keys = self.__find_keys(keys)
            self.get_action_chains().send_keys_to_element(self.element_native_action(), keys).perform()

    def element(self, locator: __WebLocator):
        return self.__BrowserActionDefinitions(locator, driver=self.__driver)

    def get_action_chains(self):
        return ActionChains(self.__driver)


