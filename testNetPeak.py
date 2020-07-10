# -*- coding: utf-8 -*-

# tested on Windows 10 64 RUS
import os
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.color import Color
# pip install -U pyautoit
import autoit

import unittest

class NetpeakPageLocators(object):

    HOME_PAGE = 'https://netpeak.ua/'
    CAREER_XPATH = '//a[@href="https://career.netpeak.ua/"]'
    I_WONT_TO_GET_JOB_XPATH = '//a[@href="https://career.netpeak.ua/hiring/"]'

class TestNetPeak(unittest.TestCase):

    def clickCareerLink(self):
        self.driver.find_element_by_xpath(NetpeakPageLocators.CAREER_XPATH).click()

    def clickIWontToGetJobLink(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH,NetpeakPageLocators.I_WONT_TO_GET_JOB_XPATH)))
        self.driver.find_element_by_xpath(NetpeakPageLocators.I_WONT_TO_GET_JOB_XPATH).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button#submit")))

    def uploadCV(self):
        buttonupload = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "upload")))
        buttonupload.click()
        # self.driver.find_element_by_id("upload").click()
        # может не работать из-за названия окна, к примеру в английской версии вместо Открытие нужно писать Open
        file_png = os.getcwd()+'\\testCV.png'
        autoit.win_wait("[CLASS:#32770;TITLE:Открытие]")
        autoit.control_set_text("[CLASS:#32770;TITLE:Открытие]", "Edit1", file_png)
        autoit.control_click("[CLASS:#32770;TITLE:Открытие]", "Button1")
        time.sleep(3)

    def fillChapter3(self):
        self.driver.find_element_by_id("inputName").send_keys("Ivan")
        self.driver.find_element_by_id("inputLastname").send_keys("Ivanovich")
        self.driver.find_element_by_id("inputEmail").send_keys("Ivanovich@gmail.com")
        self.driver.find_element_by_id("inputPhone").send_keys("+123456789")

        select = Select(self.driver.find_element_by_name("by"))
        select.select_by_value("1974")

        select = Select(self.driver.find_element_by_name("bm"))
        select.select_by_value("05")

        select = Select(self.driver.find_element_by_name("bd"))
        select.select_by_value("18")

    @classmethod
    def setUpClass(self):
        super(TestNetPeak, self).setUpClass()
        self.driver = webdriver.Chrome()
        self.driver.get(NetpeakPageLocators.HOME_PAGE)
        self.driver.maximize_window()

    def test_netpeak(self):

        self.clickCareerLink()
        self.clickIWontToGetJobLink()
        self.uploadCV()

        actual_result = self.driver.find_element_by_css_selector("div#up_file_name label").text
        expected_result = "Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf)."
        assert actual_result == expected_result, "\nactual file description is: " + actual_result + " \nexpected file description is: " + expected_result

        self.fillChapter3()

        self.driver.find_element_by_id("submit").click()

        actual_result = self.driver.find_element_by_css_selector("p.warning-fields.help-block").value_of_css_property("color")
        expected_result = Color.from_string('red').rgba
        assert actual_result == expected_result, "\nactual color is: " + actual_result + " \nexpected color is: " + expected_result

        self.driver.find_element_by_css_selector("div.logo-block a").click()
        time.sleep(5)

        actual_result = self.driver.current_url
        expected_result = NetpeakPageLocators.HOME_PAGE
        assert actual_result == expected_result, "\nactual url is: " + actual_result + " \nexpected url is: " + expected_result

    @classmethod
    def tearDownClass(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()