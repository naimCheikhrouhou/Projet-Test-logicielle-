from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class RechercheTests:

    def __init__(self, driver):
        self.driver = driver

    # TC-RCH-01 : Recherche produit existant
    def test_rch_01(self):
        wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://demo.nopcommerce.com")

        time.sleep(1.5)  # Pause visuelle

        search_box = wait.until(EC.element_to_be_clickable((By.ID, "small-searchterms")))
        search_box.send_keys("Apple MacBook Pro")
        time.sleep(2)  # Pause pour voir la saisie

        self.driver.find_element(By.CSS_SELECTOR, "button.search-box-button").click()
        time.sleep(2)  # Pause pour voir la navigation

        # Attendre les résultats avec un timeout
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
        time.sleep(1)  # Pause finale

        products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
        return len(products) > 0

    # TC-RCH-02 : Produit inexistant
    def test_rch_02(self):
        wait = WebDriverWait(self.driver, 20)

        self.driver.get("https://demo.nopcommerce.com")
        time.sleep(1.5)  # Pause visuelle

        search_box = self.driver.find_element(By.ID, "small-searchterms")
        search_box.send_keys("xxxxxxzzzzqqqq")
        time.sleep(1)  # Pause pour voir la saisie

        self.driver.find_element(By.CSS_SELECTOR, "button.search-box-button").click()
        time.sleep(2)  # Pause pour voir la navigation

        message = self.driver.find_element(By.CSS_SELECTOR, ".no-result")
        time.sleep(1)  # Pause finale
        return "No products were found" in message.text

    # TC-RCH-03 : Champ vide
    def test_rch_03(self):
        self.driver.get("https://demo.nopcommerce.com")

        # Clique sur la recherche vide
        self.driver.find_element(By.CSS_SELECTOR, "button.search-box-button").click()

        try:
            # Attendre que l’alerte Firefox apparaisse
            wait = WebDriverWait(self.driver, 5)
            alert = wait.until(EC.alert_is_present())

            # Récupérer le texte de l'alerte
            alert_text = alert.text

            # Pause pour voir l’alerte pendant 1 seconde
            time.sleep(1)

            # Fermer l’alerte
            alert.accept()

            # Vérifier que le texte correspond
            return "Please enter some search keyword" in alert_text

        except TimeoutException:
            # Si aucune alerte → test échoue
            return False

    # TC-RCH-04 : Texte trop court
    def test_rch_04(self):
        wait = WebDriverWait(self.driver, 20)
        self.driver.get("https://demo.nopcommerce.com")
        time.sleep(1.5)  # Pause visuelle


        # Saisir un terme trop court
        box = self.driver.find_element(By.ID, "small-searchterms")
        box.send_keys("ab")
        time.sleep(1.5)  # Pause visuelle


        # Cliquer sur la loupe
        self.driver.find_element(By.CSS_SELECTOR, "button.search-box-button").click()
        time.sleep(1.5)  # Pause visuelle

        try:
            # Attendre le message warning

            msg = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".warning"))
            )

            # Pause pour observer le message (optionnel)
            time.sleep(1)

            # Vérifier le texte attendu
            return "Search term minimum length is 3 characters" in msg.text

        except TimeoutException:
            # Aucun message = test échoué
            return False

    # TC-RCH-05 : Caractères spéciaux
    def test_rch_05(self):
        self.driver.get("https://demo.nopcommerce.com")
        box = self.driver.find_element(By.ID, "small-searchterms")
        box.send_keys("!@#$%")
        self.driver.find_element(By.CSS_SELECTOR, "button.search-box-button").click()

        message = self.driver.find_element(By.CSS_SELECTOR, ".no-result")
        return "No products were found" in message.text


