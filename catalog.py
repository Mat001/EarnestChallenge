__author__ = 'matjaz'
"""
    TESTING PRODUCT CATALOG CALCULATIONS

    Using your language and tools of choice, create a test suite that will verify correct
    pricing for the above catalog and all state tariffs.

    We are interested not only in the test scenarios you plan to execute but also in
    how you design your test suite. If there are opportunities to modify each page's html
    to make it more testable please let us know.
    If you have any questions about success criteria please let us know.

    1. test correct pricing for the above catalog and all state tariffs
    2. test other things: that elements are present when on second page


    PAGE OBJECT DESIGN PATTERN
    --------------------------
    Separates page elements from test logic.
    Usefulness:
    If page changes (different page) we only need to modify the
    page elements class. We don't need to modify much the class
    where tests are held. This way we keep frequently-changing-page-elements
    separate from much-less-changing test-logic. And it's cleaner and more readable.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
import time
from pyvirtualdisplay import Display
import unittest


# base class
class Page():
    def __init__(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    # to navigate to catalog page because there is no link on the confirmation page that links to calc page
    def navigate_to_calculation_page(self):
        self.driver.get('https://jungle-socks.herokuapp.com/')
        return CalculationPage(self.driver)


# Calculation page - first child class
class CalculationPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # varirables for text fields and dropdown items
    zebra = '1'
    lion = '2'
    elephant = '3'
    giraffe = '4'

    state = 'CA'

    # ============   PAGE ELEMENTS   =================
    # fill form  with data (fillitem fields with quantities and select state)
    def add_quantities(self):
        self.driver.find_element_by_id('line_item_quantity_zebra').send_keys(self.zebra)
        self.driver.find_element_by_id('line_item_quantity_lion').send_keys(self.lion)
        self.driver.find_element_by_id('line_item_quantity_elephant').send_keys(self.elephant)
        self.driver.find_element_by_id('line_item_quantity_giraffe').send_keys(self.giraffe)
        return CalculationPage(self.driver)

    def select_state(self):
        select_state = Select(self.driver.find_element_by_name('state'))    # dropdown could go in its own method?
        select_state.select_by_value(self.state)
        return CalculationPage(self.driver)

    def checkout(self):
        self.driver.find_element_by_name('commit').click()
        return ConfirmationPage(self.driver)


# Confirmation page - second child class
class ConfirmationPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # ============   PAGE ELEMENTS   =================
    def zebra_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[2]/td[3]').text

    def lion_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[3]/td[3]').text

    def elephant_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[4]/td[3]').text

    def giraffe_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[5]/td[3]').text

    # KEEP ADDING PAGE ELEMENTS HERE
    # ...


# =====   TESTS, TEST LOGIC, ASSERTIONS, TEST RUNNER
class TestCalculation(unittest.TestCase):
    def setUp(self):
        # self._display = Display(visible=1, size=(1024, 768))
        # self._display.start()
        self.driver = webdriver.Firefox()

    def test_prices(self):
        on_calculation_page = CalculationPage(self.driver)
        on_calculation_page = on_calculation_page.navigate_to_calculation_page().add_quantities().select_state()
        on_confirmation_page = on_calculation_page.checkout()
        self.assertEqual(on_confirmation_page.zebra_quantity(), on_calculation_page.zebra)
        self.assertEqual(on_confirmation_page.lion_quantity(), on_calculation_page.lion)
        self.assertEqual(on_confirmation_page.elephant_quantity(), on_calculation_page.elephant)
        self.assertEqual(on_confirmation_page.giraffe_quantity(), on_calculation_page.giraffe)

    



    def tearDown(self):
        # self._display.stop()
        self.driver.close() # play with quit()



if __name__ is "__main__":
    unittest.main()














