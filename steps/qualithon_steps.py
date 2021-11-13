from behave import *
from pages.qualithon_page import QualithonPage


@step(u'I enter the contest')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.launch_contest()
    home_obj.click_on_start_icon()
    home_obj.click_on_start_button()


@step(u'I solve the proceed button puzzle')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_proceed_button_puzzle()


@step(u'I solve the video puzzle')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_video_puzzle()


@step(u'I solve the maze puzzle')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_maze_puzzle()


@step(u'I solve the map puzzle')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_map_puzzle()


@step(u'I solve the captcha')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_captcha()


@step(u'I solve the socket puzzle')
def step_impl(context):
    home_obj = QualithonPage(context.driver)
    home_obj.solve_socket_puzzle()


@step(u'I should be having the treasure')
def step_impl(context):
    pass