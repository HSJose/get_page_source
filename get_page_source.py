# Script to get page source of a Debuggable app/channel
from appium import webdriver
from appium.options.common import AppiumOptions
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from rich import print

# Load environment variables
load_dotenv()
api_key = getenv('HEADSPIN_API_TOKEN')
app_id = getenv('APP_ID')
udid = getenv('UDID')

# Appium Load Balancer Endpoint
alb_wd = f'https://appium-dev.headspin.io:443/v0/{api_key}/wd/hub'

# Set desired capabilities
capabilities = {
    'platformName': 'tizentv',
    'appium:deviceName': 'SamsungTV',
    'appium:automationName': 'tizentv',
    'appium:udid': udid,
    'headspin:app.id': app_id
}

# convert capabilities to AppiumOptions
appium_options = AppiumOptions().load_capabilities(capabilities)
appium_options.set_capability('appium:newCommandTimeout', 300)
appium_options.set_capability('headspin:controlLock', True)
appium_options.set_capability('headspin:retryNewSessionFailure', False)

def start_appium_session() -> object:
    '''
    Start an appium session with the desired capabilities
    '''
    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=alb_wd,
            options=appium_options
        )

        session_id = driver.session_id
        print(f"Appium session started with session id: {session_id}")
    except Exception as e:
        print(f"Error starting appium session: {e}")
    
    return driver



def get_page_source(driver: object) -> str:
    '''
    get the page source of the current screen and save it to a file
    '''
    page_source = None
    try:
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        page_source = driver.page_source
        with open(f'get_page_source_{current_time}.xml', 'a') as xml_file:
            xml_file.write(page_source)

    except Exception as e:
        print(f"Error getting page source: {e}")
    
    return page_source


# we start the appium session and then have a loop that waits for keybopard input to get the page source
# this allows us to get the page source from the desired screen of the app
def main():
    driver = start_appium_session()
    some_input = input("Do you want to get page source? Press any key to continue or q to quit:")

    while some_input != 'q':
        get_page_source(driver)
        some_input = input("Press any key to get page source or q to quit:")

    if driver:
        driver.quit()


if __name__ == '__main__':
    main()
        
