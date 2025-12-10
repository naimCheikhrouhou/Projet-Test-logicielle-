from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tests.recherche_tests import RechercheTests

class SuiteRecherche:

    def __init__(self):
        options = Options()

        # Désactiver la détection webdriver
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        # Changer le user-agent pour paraître plus humain
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        )

        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        self.tests = RechercheTests(self.driver)

    def run(self):
        results = {}

        results["TC-RCH-01"] = self.tests.test_rch_01()
        """
        results["TC-RCH-02"] = self.tests.test_rch_02()
        
        results["TC-RCH-03"] = self.tests.test_rch_03()

        results["TC-RCH-04"] = self.tests.test_rch_04()
        
        results["TC-RCH-05"] = self.tests.test_rch_05()
        """
        self.driver.quit()
        return results


if __name__ == "__main__":
    suite = SuiteRecherche()
    output = suite.run()

    for test_name, result in output.items():
        print(f"{test_name} : {'PASSED' if result else 'FAILED'}")
