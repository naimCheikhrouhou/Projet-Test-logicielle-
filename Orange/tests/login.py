# tests/login.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginTest:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def _slow_type(self, element, text):
        """Simule une saisie humaine (lente)"""
        for char in text:
            element.send_keys(char)
            time.sleep(0.1)

    def tc_login_01_valid_credentials(self):
        """TC-LOGIN-01 — Login avec identifiants valides (POSITIF)"""
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Attendre que le champ username soit visible
        username_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")

        # Saisie lente
        self._slow_type(username_field, "Admin")
        self._slow_type(password_field, "admin123")
        time.sleep(0.5)
        login_btn.click()

        # Vérifier redirection vers le dashboard
        try:
            time.sleep(3)
            self.wait.until(EC.url_contains("/dashboard"))
            assert "dashboard" in driver.current_url.lower()
            print("✅ TC-LOGIN-01: Login réussi avec identifiants valides.")
        except TimeoutException:
            raise AssertionError("❌ Échec: Redirection vers le dashboard non détectée.")

    def tc_login_02_invalid_password(self):
        """TC-LOGIN-02 — Login avec mot de passe invalide (NÉGATIF)"""
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        username = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")

        self._slow_type(username, "Admin")
        self._slow_type(password, "wrongpass")
        time.sleep(0.5)
        login_btn.click()

        # Vérifier le message d'erreur
        error_msg = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']"))
        )
        assert "Invalid credentials" in error_msg.text
        print("✅ TC-LOGIN-02: Erreur affichée pour mot de passe invalide.")

    def tc_login_03_nonexistent_user(self):
        """TC-LOGIN-03 — Login avec username en majuscules (NÉGATIF)"""
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        username = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")

        # Utiliser "ADMIN" en majuscules (l'utilisateur valide est "Admin")
        self._slow_type(username, "ADMIN")
        self._slow_type(password, "admin123")
        time.sleep(0.5)
        login_btn.click()

        # Vérifier que le message d'erreur s'affiche ET qu'on reste sur la page de login
        error_msg = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']"))
        )
        assert "Invalid credentials" in error_msg.text
        assert "dashboard" not in driver.current_url.lower()
        print("✅ TC-LOGIN-03: Erreur 'Invalid credentials' affichée pour username en majuscules.")

    def tc_login_04_empty_fields(self):
        """TC-LOGIN-04 — Login avec champs vides (NÉGATIF - limite)"""
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_btn.click()

        # Vérifier les messages d'erreur sous les champs
        required_msg_username = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Required']"))
        )
        # Il y a deux "Required", mais on suppose qu'au moins un s'affiche
        assert required_msg_username.is_displayed()
        print("✅ TC-LOGIN-04: Messages 'Required' affichés pour champs vides.")

    def tc_login_05_sql_injection_attempt(self):
        """TC-LOGIN-05 — Tentative d'injection SQL dans le champ username (NÉGATIF)"""
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        username = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")

        # Injection SQL classique
        sql_payload = "' OR '1'='1"
        self._slow_type(username, sql_payload)
        self._slow_type(password, "any_password")
        time.sleep(0.5)
        login_btn.click()

        # Le système doit refuser la connexion et afficher "Invalid credentials"
        error_msg = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']"))
        )
        assert "Invalid credentials" in error_msg.text
        assert "/auth/login" in driver.current_url  # Pas de redirection
        print("✅ TC-LOGIN-05: Tentative d'injection SQL correctement rejetée.")
        # OrangeHRM accepte les espaces (il trim automatiquement), donc login réussi
        # Mais si tu veux tester un cas d’erreur, on peut forcer un échec ?
        # Ici, on note que le système est robuste → résultat POSITIF (mais ce n’est pas un bug)
        # Donc ce test est plus un test de robustesse → on vérifie qu’il ne crash pas

