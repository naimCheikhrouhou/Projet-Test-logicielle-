# suites/login.py
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.login import LoginTest
import time
import traceback


def ensure_back_to_login(driver):
    """
    Vérifie si on est sur le dashboard (ou autre page après login).
    Si oui → effectue la déconnexion pour revenir à la page de login.
    Sinon → ne rien faire.
    """
    current_url = driver.current_url
    if "/dashboard" in current_url:
        print("  → Détection : utilisateur connecté. Déconnexion en cours...")
        wait = WebDriverWait(driver, 10)

        try:
            # Clic sur le menu utilisateur
            user_dropdown = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))
            )
            time.sleep(0.4)
            user_dropdown.click()

            # Clic sur Logout
            logout_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
            )
            time.sleep(0.4)
            logout_link.click()

            # Attendre retour à la page de login
            wait.until(EC.url_contains("/auth/login"))
            print("  ✅ Retour à la page de login réussi.")

        except Exception as e:
            print(f"  ⚠️ Échec du retour à la page de login : {str(e)}")
            # On tente quand même de forcer un retour (au cas où)
            try:
                driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
                time.sleep(1)
            except:
                pass
    else:
        # On est déjà sur la page de login (ou une erreur)
        print("  → Déjà sur la page de login.")


def run_login_tests():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Edge(options=options)
    driver.execute_script("delete navigator.__proto__.webdriver")

    # Accéder à la page de login au démarrage
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(1)

    test_results = []

    try:
        login_tester = LoginTest(driver)

        test_cases = [
            ("TC-LOGIN-01 — Login valide", login_tester.tc_login_01_valid_credentials),
            ("TC-LOGIN-02 — Mot de passe invalide", login_tester.tc_login_02_invalid_password),
            ("TC-LOGIN-03 — Username en majuscules", login_tester.tc_login_03_nonexistent_user),
            ("TC-LOGIN-04 — Champs vides", login_tester.tc_login_04_empty_fields),
            ("TC-LOGIN-05 — Tentative SQL injection", login_tester.tc_login_05_sql_injection_attempt),
        ]

        for test_name, test_method in test_cases:
            print(f"\n🧪 Exécution : {test_name}")
            try:
                # S'assurer qu'on commence sur la page de login
                if "/auth/login" not in driver.current_url:
                    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
                    time.sleep(1)

                # Exécuter le test
                test_method()
                print(f"✅ {test_name} : PASS")
                test_results.append((test_name, "PASS", None))

            except Exception as e:
                error_msg = str(e)
                print(f"❌ {test_name} : FAIL — {error_msg}")
                test_results.append((test_name, "FAIL", error_msg))

            # 👇 ÉTAPE CLÉ : revenir à la page de login après chaque test
            print("  → Nettoyage post-test...")
            ensure_back_to_login(driver)
            time.sleep(1.5)  # Pause visible entre les tests

        # --- Résumé final ---
        print("\n" + "="*60)
        print("📋 RÉSUMÉ DES TESTS")
        print("="*60)
        for name, status, err in test_results:
            icon = "✅" if status == "PASS" else "❌"
            print(f"{icon} {name} → {status}")

        failed = [r for r in test_results if r[1] == "FAIL"]
        if failed:
            print(f"\n💥 {len(failed)} test(s) ont échoué. Il(s) pourrai(en)t indiquer un BUG.")
        else:
            print("\n🎉 Tous les tests sont OK !")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_login_tests()