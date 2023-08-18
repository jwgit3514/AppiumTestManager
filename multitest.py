from helper.readjson import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver as AppiumDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
import pytest
import base64
import pickle
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

settings = getcaps()

def optionInit(udid, deviceName, systemPort, appPackage, appActivity):
    options = AppiumOptions()
    options.platform_name = 'Android'
    options.automation_name = 'UIAutomator2'
    options.new_command_timeout = 60
    options.set_capability('deviceName', deviceName)
    options.set_capability('appPackage', appPackage)
    options.set_capability(
        'appActivity', appActivity)
    options.set_capability('udid', udid)
    options.set_capability('systemPort', int(systemPort))

    return options

def wait_for_element(driver, image_base64, locator = None, timeout=30):
    locator = (AppiumBy.IMAGE, image_base64)
    try:
        print('waitting for element...')
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except Exception as e:
        driver.quit()
        raise Exception(f"Element not found within {timeout} seconds: {e}")
    
def element_click_from_img(driver, img, timeout=60):
    with open(img, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    wait_for_element(driver=driver, image_base64=image_base64)
    
    accurency = 1.0
    driver.update_settings({"imageMatchThreshold": accurency})

    while True:
        try:
            element = driver.find_element(AppiumBy.IMAGE, image_base64)
            element.click()
            break 
        except Exception as e: 
            accurency -= 0.05 
            driver.update_settings({"imageMatchThreshold": accurency})

def get_target():
    try:
        with open('data_.pickle', 'rb') as f:
            data_list = pickle.load(f)            
    except Exception as e:
        print("Error!!!! : ", e)
        data_list = []

    return data_list

@pytest.mark.parametrize('udid, deviceName, systemPort', settings)
def testmy(udid, deviceName, systemPort):
    app_data = getapps()
    appPackage = app_data['package']
    appActivity = app_data['activity']

    options = optionInit(udid, deviceName, systemPort, appPackage, appActivity)

    # capabifities
    # desired_cap = {
    #     'platformName': 'Android',
    #     "appium:options": {
    #         'automationName': 'UIAutomator2',
    #         'deviceName': deviceName,
    #         'appPackage': 'com.android.settings',
    #         'appActivity': '.Settings',
    #         'udid': udid,
    #         'newCommandTimeout': 60,
    #         'systemPort': int(systemPort)
    #     },
    # }
    driver = AppiumDriver.Remote('http://localhost:4723/wd/hub', options=options)    
        
    test_list = []
    test_img_list = get_target()

    for test in test_img_list:
        test_list.append(element_click_from_img(driver, test))

    print('startting for test...')
    test_list

    driver.quit()

    # wait_for_element(driver=driver, locator=(AppiumBy.XPATH, '//*[@text="홍정원"]'))
    # driver.find_element(by=AppiumBy.XPATH, value='//*[@text="홍정원"]').click()
    # driver.quit()
  

    # driver.find_element(by=AppiumBy.XPATH,
    #                     value='//*[@text="Battery"]').click()
    # driver.quit()

    assert True
