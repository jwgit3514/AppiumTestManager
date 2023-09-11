from helper.readjson import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver as AppiumDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction
import pytest
import base64
import pickle
import time
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


def wait_for_element(driver, image_base64, locator=None, timeout=30):
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


def element_click_from_coordinate(driver, x, y, timeout=60):
    TouchAction(driver).tap(None, x, y, 1).perform()
    pass


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
    driver = AppiumDriver.Remote(
        'http://localhost:4723/wd/hub', options=options)

    driver.press

    time.sleep(5)

    test_list = []
    test_target_list = get_target()

    # flag 1 -> tap
    # flag 2 -> img
    # ...

    for i in range(len(test_target_list)):
        if test_target_list[i]['flag'] == 1:
            print('flag : ', test_target_list[i]['flag'])
            test_list.append(element_click_from_img(
                driver, test_target_list[i]['img']))
        elif test_target_list[i]['flag'] == 2:
            print('flag : ', test_target_list[i]['flag'])
            test_list.append(element_click_from_coordinate(
                driver, x=test_target_list[i]['x'], y=test_target_list[i]['y']))

    print('startting for test...', test_list)
    test_list

    time.sleep(10)

    driver.quit()

    # wait_for_element(driver=driver, locator=(AppiumBy.XPATH, '//*[@text="홍정원"]'))
    # driver.find_element(by=AppiumBy.XPATH, value='//*[@text="홍정원"]').click()
    # driver.quit()

    # driver.find_element(by=AppiumBy.XPATH,
    #                     value='//*[@text="Battery"]').click()
    # driver.quit()

    assert True


def save_pick(insert_data):
    try:
        with open('data_.pickle', 'rb') as f:
            data_list = pickle.load(f)
    except Exception as e:
        print("Error!!!! : ", e)
        data_list = []
    # data = [{'flag':'1', 'x':'123', 'y':'456'},
    #         {'flag':'2', 'path':'D:/a/b/c/adf.png'},
    #         {'flag':'1', 'x':'789', 'y':'101112'}]
    data = insert_data
    data_list.append(data)
    with open('data_.pickle', 'wb') as f:
        pickle.dump(data_list, f)


def test():
    test_list = []
    test_target_list = get_target()
    # flag 1 -> tap
    # flag 2 -> img
    # ...
    print(test_target_list)
    for i in range(len(test_target_list)):
        if test_target_list[i]['flag'] == 1:
            print(test_target_list[i]['img'])
        elif test_target_list[i]['flag'] == 2:
            pass
    print('startting for test...', test_list)


if __name__ == "__main__":
    save_pick({'flag': 1, 'x': '123', 'y': '456'})
    save_pick({'flag': 2, 'path': 'D:/a/b/c/adf.png'})
    save_pick({'flag': 1, 'x': '789', 'y': '101112'})
    test()
