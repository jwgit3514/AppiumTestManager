from helper.readjson import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver as AppiumDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
import pytest
import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


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


def wait_for_element(driver, locator, timeout=60):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except Exception as e:
        driver.quit()
        raise Exception(f"Element not found within {timeout} seconds: {e}")


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

    with open('./cropped_2.png', 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    driver = AppiumDriver.Remote(
        'http://localhost:4723/wd/hub', options=options)
    
    accurency = 0.9
    driver.update_settings({"imageMatchThreshold": accurency})

    while True:
        try:
            element = driver.find_element(AppiumBy.IMAGE, image_base64)
            element.click()
            break # 이미지를 찾으면 클릭 후에 무한 반복문 종료
        except Exception as e: #이미지를 찾지못하면 NoSuchElementException이 발생하는데 이것을 catch
            accurency -= 0.05 # 찾고자하는 이미지와, 스크린 상에서의 이미지의 정확도(매칭률)을 조정하고
            driver.update_settings({"imageMatchThreshold": accurency}) # 정확도 업데이트 후 다시 반복 시작

    # wait_for_element(driver=driver, locator=(AppiumBy.XPATH, '//*[@text="홍정원"]'))
    # driver.find_element(by=AppiumBy.XPATH, value='//*[@text="홍정원"]').click()
    # driver.quit()
  

    # driver.find_element(by=AppiumBy.XPATH,
    #                     value='//*[@text="Battery"]').click()
    # driver.quit()

    assert True
