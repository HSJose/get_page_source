# Script to get page source of a Debuggable app/channel
from appium import webdriver
from appium.options.common import AppiumOptions
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from time import sleep
from rich import print

# Load environment variables
load_dotenv()
api_key = getenv('HEADSPIN_API_TOKEN')
app_id = getenv('APP_ID')
udid = getenv('UDID')

print(app_id)
print(udid)

# Appium Load Balancer Endpoint
alb_wd = f'https://appium-dev.headspin.io:443/v0/{api_key}/wd/hub'

# Set desired capabilities
capabilities = {
    'platformName': 'roku',
    'appium:automationName': 'roku',
    'appium:deviceName': 'roku',
    'headspin:app.id': app_id,
    'appium:udid': udid,
}

# convert capabilities to AppiumOptions
appium_options = AppiumOptions().load_capabilities(capabilities)
appium_options.set_capability('appium:newCommandTimeout', 600)
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
        page_source = driver.page_source

    except Exception as e:
        print(f"Error getting page source: {e}")
    
    return page_source


def write_page_source_to_file(page_source: str, filename: str):
    # check if page_source is None
    if not page_source:
        print("No page source to write to file.")
        return
    
    # check if filename is None or empty
    if not filename:
        print("Filename cannot be None or empty.")
        return
    
    try:
        with open(filename, 'w') as file:
            file.write(page_source)
        print(f"Page source written to {filename}")
    except Exception as e:
        print(f"Error writing page source to file: {e}")


def press_key(driver, key: str):
    '''
    Press a key on the Roku device
    '''

    ALLOWED_KEYS = (
        "Home",
        "Rev",
        "Fwd",
        "Play",
        "Select",
        "Left",
        "Right",
        "Down",
        "Up",
        "Back",
        "InstantReplay",
        "Info",
        "Backspace",
        "Search",
        "Enter",
    )

    normalized_key = key[0].upper() + key[1:]
    if normalized_key not in ALLOWED_KEYS:
        raise ValueError(f"Invalid key: '{normalized_key}'. Must be one of: {', '.join(ALLOWED_KEYS)}")
    
    try:
        driver.execute_script('roku: pressKey', {'key': normalized_key})
        print(f"Pressed key: {normalized_key}")
        sleep(1)
    except Exception as e:
        print(f"Error pressing key '{normalized_key}': {e}")

def prompt_user() -> str:
    return input("Press any key to get page source or 'q' to quit: ").strip().lower()

def save_page_source(source: str):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'page_source_{timestamp}.xml'
    write_page_source_to_file(source, filename)
    print(f"Saved updated page source to {filename}")

def refresh_and_check_source(driver, current_source: str) -> str:
    # Try to shake the screen by triggering minor input
    press_key(driver, 'Down')
    press_key(driver, 'Up')
    refreshed_source = get_page_source(driver)

    if refreshed_source != current_source:
        save_page_source(refreshed_source)
        return refreshed_source
    else:
        print("No change in page source.")
        return current_source

# we start the appium session and then have a loop that waits for keybopard input to get the page source
# this allows us to get the page source from the desired screen of the app
def main():

    driver = None

    try:
        driver = start_appium_session()
        current_source = None

        while True:
            user_input = prompt_user()
            if user_input == 'q':
                break

            page_source = get_page_source(driver)

            if current_source is None or current_source != page_source:
                current_source = page_source
                save_page_source(current_source)
            else:
                current_source = refresh_and_check_source(driver, current_source)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    main()
        
