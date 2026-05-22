from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user opens website
        self.browser.get(self.live_server_url)
        # he resizes browser window
        self.browser.set_window_size(1024, 768)

        # he sees text box positioned at center
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + (inputbox.size["width"] / 2),
            512,
            delta=30
        )

        # he creates a new to-do item
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("1: testing")
        
        # he still sees text box positioned at center
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=30
        )
