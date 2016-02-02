PRODUCT CATALOG TESTING
=========================

Firstly, I know Java, but since I'm currently more comfortable with Python I wrote this 
these tests in Python, just for this assignment. I hope the code is readable enough and 
explanation below at least satisfactory to a degree. Otherwise please email me or call me.
Happy to answer questions.

Explanations and instructions

Tu run:
Instructions for MAC:
- download from github
- put three files tests.py, page_objects.py, data.py into a directory of your choice (home is best)
- on MAC install Python version 3 
- install pip3 (brew install pip3)
- install selenium: pip3 install selenium (yuo need selenium library) 
- go to directory where you put three Python files (use CD command).
- run in terminal: python3 -m unittest tests.py

Project consists of:
tests.py file which contains tests
page_object.py file which contains classes with web elements
data.py file which contains catalog data that was provided with assignment

data.py file is not really used, it's purpose is only to provide state tax information with get_state_tax() function

Project uses page object design pattern.
I used this pattern because it's a good practice to separate test logic from the web elements.
Classes for each page (Calculation page-starting page, Confirmation page, Error page) are provided in page_object.py file.
Test logic is written in tests.py file in different test classes.

Page class let's us use only one instance of the webdriver across multiple inherited page objects.
We create one instance of webdriver and through the Page base class this instance of the webdriver is propagated
using inheritance to other page classes. This way we avoid creating and opening browsers in each page class.

Webdriver class in tests.py file is also a base class but for tests. We use it to set up setUp and tearDown methods
only there and not in test classes. This increases readability of tests. I also instantiated an instance of webdriver in
Webdriver class to avoid instantiating it in test classes, again for readability.
the path of webdriver instance is Webdriver class -> Page class -> CalculationPage class, ConfirmationPage class, 
Error class (using inheritance mechanism).

I believe tests with assertions should very simple and easy to read. Methods chained by dot notation and reading like plain English.
I have seen the term DSL = domain specific language used before for the way how tests are written.

Tests in tests.py file are separated into a test suite with five clases:
- TestCalulations
- TestDisplay
- TestEdgeCases
- TestFormat
- TestInventoryLimit

I could run it as one test class, but separating tests into different common groups made more sense and it's more clear and readable.

- TestCalulations = tests that calculations are correct, subtotal, tax, total, total when taxes for different states are used
- TestDisplay = tests that displayed prices and entered values match on first page and confirmation page
- TestEdgeCases = tests when no data is entered, when no state is selected etc.
- TestFormat = tests with strings and special characters entered instead of integers, negative numbers
- TestInventoryLimit = tests that assert that user can't order more items than in stock

I wanted to implement also data drived testing. For that I would test all combinations of entered values, populated fields and 
not-populated fields and states to see if any cross-selections yield defects.
In time I had I wasn't able to do it yet. I also think I would have to alter the program desig a bit.

In some tests like when special characters are entered into item fields I used the total or subtotal amount to confirm that special 
characters didn't interfere with calculations. The other, easier way could be to assert that only item prices of items that
were entered digits were showing on confirmation page. But since payment/finance is involved in this testing I rather tested 
all-the-way through the calculation itself.

My goal was to make tests short and readable. For my standards they are still to long and verbose.

All tests except one pass. The failed test is in class TestInventoryLimit which tests that user can't
 order more items than in stock. But the program doesn't have this safeguard so the test fails.
 
I wasn't quite sure

Testability of the web pages could be improved if table elements had id-s as well.
Using xpaths is not reliable because when position of an element changes, the xpath breaks and xpath then needs 
to be updated in the code which requires time. 
 
Tests are ran from the MAC or Linux command line using: python3 -m unittest tests.py

I hope these instructions provide enough information for the installation, running and review of the code.

