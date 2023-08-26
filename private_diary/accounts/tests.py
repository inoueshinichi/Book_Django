# from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium import webdriver

# Chromeを操作
# driver = webdriver.Chrome()
# # Firefoxを操作
# driver = webdriver.Firefox()

class TestLogin(LiveServerTestCase):

    @classmethod
    def setupClass(cls):
        super().setUpClass() # 注意 親クラスのメソッドを呼び出しておく
        cls.selenium = WebDriver(service='/Users/inoueshinichi/Documents/ChromeDirver_x86_64/chromedriver')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass() # 注意 親クラスのメソッドを呼び出しておく

    def test_login(self):
        # ログインページを開く
        self.selenium.get("http://localhost:8000/" + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name('login')
        username_input.send_key('inoue.shinichi.1800@gmail.com')
        password_input = self.selenium.find_element_by_name('faint180sx')
        password_input.send_keys('faint180sx')
        self.selenium.find_element_by_class_name('btn').click()

        # ページタイトルの検証
        self.assertEquals("日記一覧 | Private Diary", self.selenium.title)

