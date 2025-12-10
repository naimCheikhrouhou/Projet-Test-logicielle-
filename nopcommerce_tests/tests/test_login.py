""" 
✔️ Champs vides
✔️ Email invalide
✔️ Mot de passe trop court
✔️ Login valide / invalide
✔️ Assertions
✔️ Structure propre pour les tests 
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ________________________________________________________________
class TestNopCommerceLogin:

    def __init__(self):
        # Initialize the Edge driver
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown(self):
        self.driver.quit()

    # ---------- TEST 1 : Empty fields ----------
    def test_login_empty_fields(self):
        self.driver.get("https://demo.nopcommerce.com/login")
        time.sleep(1)

        self.driver.find_element(By.CSS_SELECTOR, "button.login-button").click()

        try:
            error = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".message-error"))
            )
            print("✔ Empty fields → error detected:", error.text)
            return True
        except TimeoutException:
            print("❌ Error message not found!")
            return False

    # ---------- TEST 2 : Invalid email ----------
    def test_login_invalid_email_format(self):
        self.driver.get("https://demo.nopcommerce.com/login")
        self.driver.find_element(By.ID, "Email").send_keys("naim@wrong")
        self.driver.find_element(By.ID, "Password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button.login-button").click()

        try:
            error = self.wait.until(
                EC.visibility_of_element_located((By.ID, "Email-error"))
            )
            assert "Wrong email" in error.text
            print("✔ Invalid email → error detected")
            return True
        except TimeoutException:
            print("❌ Error message not found!")
            return False

    # ---------- TEST 3 : Short password ----------
    def test_short_password(self):
        self.driver.get("https://demo.nopcommerce.com/login")
        self.driver.find_element(By.ID, "Email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "Password").send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, "button.login-button").click()

        try:
            error = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".message-error"))
            )
            assert "Login was unsuccessful" in error.text
            print("✔ Short password → error detected")
            return True
        except TimeoutException:
            print("❌ Error message not found!")
            return False

    # ---------- TEST 4 : Wrong credentials ----------
    def test_login_wrong_credentials(self):
        self.driver.get("https://demo.nopcommerce.com/login")
        self.driver.find_element(By.ID, "Email").send_keys("wrong@example.com")
        self.driver.find_element(By.ID, "Password").send_keys("wrongpass")
        self.driver.find_element(By.CSS_SELECTOR, "button.login-button").click()

        try:
            error = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".message-error"))
            )
            assert "Login was unsuccessful" in error.text
            print("✔ Wrong credentials → error detected")
            return True
        except TimeoutException:
            print("❌ Error message not found!")
            return False

    # ---------- TEST 5 : Valid login ----------
    def test_login_valid(self):
        self.driver.get("https://demo.nopcommerce.com/login")
        self.driver.find_element(By.ID, "Email").send_keys("TON_EMAIL_ICI")
        self.driver.find_element(By.ID, "Password").send_keys("TON_MDP_ICI")
        self.driver.find_element(By.CSS_SELECTOR, "button.login-button").click()

        time.sleep(2)
        if "My account" in self.driver.page_source:
            print("✔ Valid login → success")
            return True
        else:
            print("❌ Login failed")
            return False


# ------------------------ MAIN ------------------------
if __name__ == "__main__":
    tests = TestNopCommerceLogin()

    tests.test_login_empty_fields()
    tests.test_login_invalid_email_format()
    tests.test_short_password()
    tests.test_login_wrong_credentials()
    tests.test_login_valid()

    tests.teardown()
