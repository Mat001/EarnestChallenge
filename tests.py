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
import logging
from page_objects import CalculationPage
import test

# base class for webdriver
class WebDriver(unittest.TestCase):
    def setUp(self):
        # self._display = Display(visible=0, size=(1024, 768))  # uncomment for headless browser
        # self._display.start()      uncomment for headless browser
        self.driver = webdriver.Firefox()
        self.on_calculation_page = CalculationPage(self.driver)

    def tearDown(self):
        # self._display.stop()  # uncomment for headless browser
        self.driver.quit()



# =====   TESTS, TEST LOGIC, ASSERTIONS, TEST RUNNER
class TestCalculation(WebDriver):

    # ==========   TESTS FOR CALCULATIONS   ===========
    def test_subtotal(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        subtotal_zebra = on_confirmation_page.price_zebra() * on_confirmation_page.quantity_zebra()
        subtotal_lion = on_confirmation_page.price_lion() * on_confirmation_page.quantity_lion()
        subtotal_elephant = on_confirmation_page.price_elephant() * on_confirmation_page.quantity_elephant()
        subtotal_giraffe = on_confirmation_page.price_giraffe() * on_confirmation_page.quantity_giraffe()

        subtotal_expected = subtotal_zebra + subtotal_lion + subtotal_elephant + subtotal_giraffe
        subtotal_expected = round(subtotal_expected, 4)
        subtotal_displayed = on_confirmation_page.subtotal()
        self.assertEqual(subtotal_expected, subtotal_displayed)


    def test_tax_ca(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        # expected taxes
        taxes_expected = on_confirmation_page.subtotal() * self.on_calculation_page.tax_rate('CA')
        taxes_expected = round(taxes_expected, 4)   # round decimal number to 4 digits
        # displayed taxes
        taxes_displayed = on_confirmation_page.taxes()
        self.assertEqual(taxes_expected, taxes_displayed)

    def test_tax_ny(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='NY')

        on_confirmation_page = self.on_calculation_page.checkout()

        # expected taxes
        taxes_expected = on_confirmation_page.subtotal() * self.on_calculation_page.tax_rate('NY')
        taxes_expected = round(taxes_expected, 4)  # round decimal number to 4 digits
        # displayed taxes
        taxes_displayed = on_confirmation_page.taxes()
        self.assertEqual(taxes_expected, taxes_displayed)

    def test_tax_mn(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='MN')

        on_confirmation_page = self.on_calculation_page.checkout()

        # expected taxes
        taxes_expected = on_confirmation_page.subtotal() * self.on_calculation_page.tax_rate('MN')
        taxes_expected = round(taxes_expected, 4)  # round decimal number to 4 digits
        # displayed taxes
        taxes_displayed = on_confirmation_page.taxes()
        print('MN: ', taxes_expected, taxes_displayed)
        self.assertEqual(taxes_expected, taxes_displayed)

    def test_tax_co(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='CO')

        on_confirmation_page = self.on_calculation_page.checkout()

        # expected taxes
        taxes_expected = on_confirmation_page.subtotal() * self.on_calculation_page.tax_rate('CO')
        taxes_expected = round(taxes_expected, 4)  # round decimal number to 4 digits
        # displayed taxes
        taxes_displayed = on_confirmation_page.taxes()
        self.assertEqual(taxes_expected, taxes_displayed)


    def test_total(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        total_expected = on_confirmation_page.subtotal() + on_confirmation_page.taxes()
        total_expected = round(total_expected, 4)
        total_displayed = on_confirmation_page.total()

        self.assertEqual(total_displayed, total_expected)


class TestFormat(WebDriver):
    # ==========   TESTS RELATED TO THE FORMAT AND OF ENTERED VALUES   ===========
    # if all fields contain strings, then totl should be zero
    def test_item_where_entered_characters_should_no_be_calculated(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA='aaaaa', LION='bbbbb', ELEPHANT='ccccc', GIRAFFE='ddddd') \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.total(), 0.00)


    def test_item_whereentered_special_chars_should_not_be_calculated(self):
        # calculated subtotal is proof that zebra and lion with special characters were not included into calculation
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=1, ELEPHANT='@#$', GIRAFFE='>><"') \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        subtotal_zebra = on_confirmation_page.price_zebra() * on_confirmation_page.quantity_zebra()
        subtotal_lion = on_confirmation_page.price_lion() * on_confirmation_page.quantity_lion()

        subtotal_expected = subtotal_zebra + subtotal_lion
        subtotal_expected = round(subtotal_expected, 4)
        subtotal_displayed = on_confirmation_page.subtotal()
        self.assertEqual(subtotal_expected, subtotal_displayed)


    def test_entered_decimal_number_should_have_decimal_part_truncated(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1.5, LION=2.7, ELEPHANT=3.3, GIRAFFE=1.934) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        # assert that confirmation page shows truncated quantities
        self.assertEqual(on_confirmation_page.quantity_zebra(), 1)
        self.assertEqual(on_confirmation_page.quantity_lion(), 2)
        self.assertEqual(on_confirmation_page.quantity_elephant(), 3)
        self.assertEqual(on_confirmation_page.quantity_giraffe(), 1)

        # assert that truncated quantities are used in calculation
        subtotal_expected = on_confirmation_page.price_zebra()*1 +\
                            on_confirmation_page.price_lion()*2 + \
                            on_confirmation_page.price_elephant()*3 + \
                            on_confirmation_page.price_giraffe()*1

        subtotal_expected = round(subtotal_expected, 4)
        subtotal_displayed = on_confirmation_page.subtotal()
        self.assertEqual(subtotal_expected, subtotal_displayed)

    def test_negative_numbers_ignored_in_calculation(self):
        # calculated subtotal is proof that zebra and lion with negative numbers were not included into calculation
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=1, ELEPHANT=-1, GIRAFFE=-3) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        subtotal_zebra = on_confirmation_page.price_zebra() * on_confirmation_page.quantity_zebra()
        subtotal_lion = on_confirmation_page.price_lion() * on_confirmation_page.quantity_lion()

        subtotal_expected = subtotal_zebra + subtotal_lion
        subtotal_expected = round(subtotal_expected, 4)
        subtotal_displayed = on_confirmation_page.subtotal()
        self.assertEqual(subtotal_expected, subtotal_displayed)


class TestInventoryLimit(WebDriver):
    # ==========   TESTS RELATED INVENTORY LIMIT   ===========
    # this test should fail because currently user can order more items than specified in stock
    # test that you can't proceed to confirmation page if order is higher than stock
    def test_quantities_higher_than_stock_not_allowed(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=24, LION=13, ELEPHANT=4, GIRAFFE=16) \
            .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertNotEqual(on_confirmation_page.page_title(), 'Please Confirm Your Order')


class TestDisplay(WebDriver):
    # ==========   TESTS RELATED TO CORRECTLY DISPLAYING VALUES   ===========
    def test_entered_quantities_display_on_confirmation_page(self):
        self.on_calculation_page \
                .navigate_to_calculation_page() \
                .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
                .select_state(STATE='CA')

        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.quantity_zebra(), 1)
        self.assertEqual(on_confirmation_page.quantity_lion(), 2)
        self.assertEqual(on_confirmation_page.quantity_elephant(), 3)
        self.assertEqual(on_confirmation_page.quantity_giraffe(), 4)

    def test_displayed_prices_on_both_pages_match(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4) \
            .select_state(STATE='CA')

        price_zebra_calc_page = self.on_calculation_page.get_price_zebra_calc_page()
        price_lion_calc_page =  self.on_calculation_page.get_price_lion_calc_page()
        price_eleph_calc_page =  self.on_calculation_page.get_price_elephant_calc_page()
        price_girrafe_calc_page = self.on_calculation_page.get_price_giraffe_calc_page()

        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.price_zebra(), price_zebra_calc_page)
        self.assertEqual(on_confirmation_page.price_lion(), price_lion_calc_page)
        self.assertEqual(on_confirmation_page.price_elephant(), price_eleph_calc_page)
        self.assertEqual(on_confirmation_page.price_giraffe(), price_girrafe_calc_page)


class TestEdgeCases(WebDriver):
    # ========   TESTING EDGE CASES   =============
    def test_nothing_entered_should_take_to_error_page(self):
        self.on_calculation_page.navigate_to_calculation_page()
        on_error_page = self.on_calculation_page.checkout()
        self.assertEqual(on_error_page.error_message(), 'We\'re sorry, but something went wrong.')

    def test_quantites_all_selected_but_no_state_should_take_to_error_page(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities(ZEBRA=1, LION=2, ELEPHANT=3, GIRAFFE=4)
            # no state selected

        # should redirect to error page
        on_error_page = self.on_calculation_page.checkout()
        self.assertEqual(on_error_page.error_message(), 'We\'re sorry, but something went wrong.')

    def test_state_selected_but_no_quantities_should_total_zero(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .select_state(STATE='CA')

        # should ive total as zero
        on_confirmation_page = self.on_calculation_page.checkout()

        total_expected = on_confirmation_page.subtotal() + on_confirmation_page.taxes()
        total_displayed = on_confirmation_page.total()
        self.assertEqual(total_displayed, total_expected)
        self.assertEqual(total_displayed, 0.00)



if __name__ is "__main__":
    """ Run test suites """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCalculation))
    suite.addTest(unittest.makeSuite(TestDisplay))
    suite.addTest(unittest.makeSuite(TestEdgeCases))
    suite.addTest(unittest.makeSuite(TestFormat))
    suite.addTest(unittest.makeSuite(TestInventoryLimit))
    runner = unittest.TextTestRunner()
    runner.run(suite)














