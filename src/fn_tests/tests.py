from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

# fun fact: all-caps is a convention for constants
MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        if test_server := os.environ.get("TEST_SERVER"):
            self.live_server_url = "http://" + test_server
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_starting_a_todo_list(self):
        # user opens the website
        self.browser.get(self.live_server_url)
        
        # he sees the tab title and a header
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # FIRST ITEM
        # he is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # he types into the text box and hits enter
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        # the page updates and now he sees his new to-do item
        self.wait_for_row_in_table("1: Buy eggs and milk")

        # SECOND ITEM
        # he is invited to enter a to-do item again
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # he types into the text box and hits enter
        inputbox.send_keys("Buy cheese and bread")
        inputbox.send_keys(Keys.ENTER)
        # the page updates and now he sees both his to-do items
        self.wait_for_row_in_table("2: Buy cheese and bread")
        self.wait_for_row_in_table("1: Buy eggs and milk")

    def test_multiple_users_and_lists(self):
        # user 1 opens the website
        self.browser.get(self.live_server_url)
        # he creates a new to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        # he sees his new to-do item
        self.wait_for_row_in_table("1: Buy eggs and milk")
        
        # his list has a unique URL
        first_user_url = self.browser.current_url
        self.assertRegex(first_user_url, "/lists/.+")

        # user 2 opens the website
        self.browser.get(self.live_server_url)
        # he doesn't see user 1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy eggs and milk", page_text)
        
        # he creates a new to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy cheese and bread")
        inputbox.send_keys(Keys.ENTER)
        # he sees his new to-do item
        self.wait_for_row_in_table("1: Buy cheese and bread")

        # his list has a unique URL
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, "/lists/.+")
        
        # still no trace of user 1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy eggs and milk", page_text)
        self.assertIn("Buy cheese and bread", page_text)
        
        # both users have different URLs
        self.assertNotEqual(first_user_url, second_user_url)
    
    def test_layout_and_styling(self):
        # user opens the website
        self.browser.get(self.live_server_url)
        # he resizes the window
        self.browser.set_window_size(1024, 768)

        # he sees the text box at the center
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + (inputbox.size["width"] / 2),
            512,
            delta=30
        )

        # he creates a new to-do item
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: testing")
        
        # he still sees the text box at the center
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=30
        )
