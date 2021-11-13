from utilities.web import BrowserUtils
from utilities.locator_strategies import xpath, tagName, image, id
from utilities.maze import Maze
from utilities.logs import Logs
import pyautogui
from utilities.web_socket import WebSocket


class QualithonPage:

    def __init__(self, driver):
        self.start_icon = xpath("//img[@src='/static/door.png']")
        self.start_button = xpath("//button[@id='start']")
        self.proceed_button = lambda button_number: xpath(f"//button[@id='c1submitbutton{button_number}']")
        self.youtube_play_button = xpath("//button[contains(@class,'large-play-button')]")
        self.youtube_iframe = id("aVideoPlayer")
        self.video_section = tagName("video")
        self.mute_button = xpath("//button[contains(@class,'mute-button')]")
        self.video_proceed_button = xpath("//button[@id='aVideoSubmit']")
        self.up_arrow_button = xpath("//i[text()='arrow_upward']")
        self.down_arrow_button = xpath("//i[text()='arrow_downward']")
        self.left_arrow_button = xpath("//i[text()='arrow_back']")
        self.right_arrow_button = xpath("//i[text()='arrow_forward']")
        self.maze_submit_button = id("crystalMazeFormSubmit")
        self.maze_section = id("maze")
        self.map_section = xpath("(//div[@id='map']//img)[2]")
        self.map_submit_button = id("mapsChallengeSubmit")
        self.captcha_image = id("notABotCaptchaImg")
        self.captcha_response = id("notABotCaptchaResponse")
        self.captcha_submit = id("notABotCaptchaSubmit")
        self.ws_url = id("wsurl")
        self.msg_content = xpath("//div[contains(@class,'yellow lighten')]")
        self.token_textbox = id("socketGateMessage")
        self.socket_puzzle_submit_button = xpath("//button[text()='Submit']")
        self.treasure_image = xpath("//img[contains(@src, 'treasure')]")
        self.utils = BrowserUtils(driver)

    def launch_contest(self):
        self.utils.launchUrl("http://54.80.137.197:5000/")

    def click_on_start_icon(self):
        self.utils.element(self.start_icon).scroll_to_element().click()

    def click_on_start_button(self):
        self.utils.element(self.start_button).click()

    def click_on_proceed_button(self, button_number):
        self.utils.element(self.proceed_button(button_number)).click()

    def solve_proceed_button_puzzle(self):
        try:
            for num in range(1, 6):
                self.click_on_proceed_button(num)
        except Exception:
            Logs.log_error("Error while solving proceed puzzle")

    def click_on_video_play_button(self):
        self.utils.element(self.youtube_play_button).click()

    def click_on_mute_button(self):
        self.utils.element(self.mute_button).click()

    def hover_video(self):
        self.utils.element(self.video_section).mouse_hover()

    def click_on_video_proceed_button(self):
        self.utils.element(self.video_proceed_button).click()

    def switch_youtube_iframe(self):
        self.utils.element(self.youtube_iframe).scroll_to_element()
        self.utils.switch_to_iframe(self.youtube_iframe)

    def solve_video_puzzle(self):
        self.switch_youtube_iframe()
        self.click_on_video_play_button()
        self.utils.sleep_for(10)
        self.hover_video()
        self.click_on_mute_button()
        self.utils.switch_to_default()
        self.click_on_video_proceed_button()

    def get_maze_data(self):
        self.utils.sleep_for(5)
        data = []
        self.utils.wait_until_page_is_fully_loaded()
        # return self.utils.execute_script("return data")
        for tr in self.utils.element(xpath("//table[@id='maze']/tr")).elements_native_action():
            tr_data = []
            for td in tr.find_elements_by_tag_name("td"):
                if 'black' in td.get_attribute('class'):
                    tr_data.append(1)
                elif 'deep-purple' in td.get_attribute('class'):
                    tr_data.append(4)
                elif 'blue-grey' in td.get_attribute('class'):
                    tr_data.append(2)
                elif 'green' in td.get_attribute('class'):
                    tr_data.append(3)
                else:
                    tr_data.append(0)
            data.append(tr_data)
        return data


    def click_right_arrow_button(self):
        self.utils.element(self.right_arrow_button).click()

    def click_left_arrow_button(self):
        self.utils.element(self.left_arrow_button).click()

    def click_up_arrow_button(self):
        self.utils.element(self.up_arrow_button).click()

    def click_down_arrow_button(self):
        self.utils.element(self.down_arrow_button).click()

    def click_on_maze_submit_button(self):
        self.utils.element(self.maze_submit_button).click()

    def solve_maze_puzzle(self):
        maze_data = self.get_maze_data()
        Logs.log_info(maze_data)
        self.utils.element(self.maze_section).scroll_to_element()
        directions = Maze(maze_data).get_direction()
        for direction in directions:
            if direction == 'right':
                self.click_right_arrow_button()
            elif direction == 'left':
                self.click_left_arrow_button()
            elif direction == 'up':
                self.click_up_arrow_button()
            elif direction == 'down':
                self.click_down_arrow_button()
        self.click_on_maze_submit_button()
        self.utils.sleep_for(10)

    def click_on_map_section(self):
        self.utils.element(self.map_section).click()

    def move_pointer_to_india(self):
        self.utils.get_action_chains().send_keys('i').perform()
        self.utils.sleep_for(3)
        for _ in range(0, 37):
            pyautogui.press('right')
        for _ in range(0, 8):
            pyautogui.press('up')

    def click_on_map_submit_button(self):
        self.utils.element(self.map_submit_button).click()

    def solve_map_puzzle(self):
        self.click_on_map_section()
        self.move_pointer_to_india()
        self.click_on_map_submit_button()

    def get_captcha_data(self):
        self.utils.sleep_for(10)
        val = self.utils.execute_script("return captcha.toString();")
        captcha = val.split()[2].replace('console.log("', "").replace('");', "")
        Logs.log_info(f"Captcha is {captcha}")
        return captcha

    def enter_captcha(self, text):
        self.utils.element(self.captcha_response).fill_text(text)

    def click_on_submit_captcha(self):
        self.utils.element(self.captcha_submit).click()

    def solve_captcha(self):
        captcha = self.get_captcha_data()
        self.enter_captcha(captcha)
        self.click_on_submit_captcha()

    def get_ws_url(self):
        return str(self.utils.element(self.ws_url).get_text()).strip()

    def get_message_content(self):
        return str(self.utils.element(self.msg_content).get_text()).strip()

    def fetch_access_token(self):
        return WebSocket.send_message(server=self.get_ws_url(), message=self.get_message_content())

    def enter_access_token(self, text):
        self.utils.element(self.token_textbox).fill_text(text)

    def click_on_token_submit_button(self):
        self.utils.element(self.socket_puzzle_submit_button).click()

    def solve_socket_puzzle(self):
        self.enter_access_token(self.fetch_access_token())
        self.click_on_token_submit_button()

    def validate_treasure_is_displayed(self):
        self.utils.sleep_for(10)
        self.utils.element(self.treasure_image).validate_element_is_present()
