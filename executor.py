import os
import shutil
import subprocess
from utilities.common import get_root_directory
from rich.console import Console
from rich.panel import Panel
from rich.align import Align


console = Console()


def print_console_header(header_name):
    header = Panel(Align.center(header_name), style="bold magenta", height=3)
    console.print(header)


def clean_temp_and_create_temp_allure_reports():
    folder = os.path.join(get_root_directory(), 'temp')
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete contents in temp folder %s. Reason: %s' % (file_path, e))
    else:
        os.mkdir(folder)
    os.mkdir(os.path.join(get_root_directory(), 'temp', 'allure'))


def execute():
    print_console_header("QUALITHON - 2021")
    clean_temp_and_create_temp_allure_reports()
    report_folder = os.path.join(get_root_directory(), 'temp', 'allure')
    command = f'behave --tags run -f allure_behave.formatter:AllureFormatter -o {report_folder}'
    subprocess.run(command, cwd=get_root_directory(), shell=True)
    generate_allure_report(results_path=report_folder, html_report_path=os.path.join(get_root_directory(), 'results', 'allure'))


def generate_allure_report(results_path, html_report_path):
    command = os.path.join(get_root_directory(), 'external_plugins', 'AllureCli', 'bin',
                           'allure.bat') + ' generate ' + results_path + ' -o ' + html_report_path + ' --clean'
    subprocess.run(command, cwd=get_root_directory(), shell=True)

execute()