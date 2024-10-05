from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd
from pathlib import Path
import os
import json
import time


class VentaIdeal:
    """Extracción de la venta diaria"""

    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_experimental_option("prefs", self.options_chrome())
        self.driver = Chrome(options=self.options)
        self.credenciales = self._cargar_credenciales()

    def _cargar_credenciales(self):
        with open(r"credenciales\mc1.json") as file:
            return json.load(file)
        
    def options_chrome(self):
        """Configuración del driver para elegir la carpeta de descargas"""
        
        folder_download = Path(os.getcwd(), "Download")
        if not os.path.exists(folder_download):
            os.makedirs(folder_download)

        return {
            "download.default_directory": str(folder_download.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

    def login_mc1(self):
        url = "https://prodweb-bimbo-las.mc1.com.br/WTM_Client/Form/Run/Custom_Check_Orders_BIMBO?menuItem=1642615056076"
        
        self.driver.get(url)
        self.driver.find_element(By.ID, "UserName").send_keys(self.credenciales["user"])
        self.driver.find_element(By.ID, "Password").send_keys(self.credenciales["password"])
        self.driver.find_element(By.ID, "Domain").send_keys(self.credenciales["domain"])
        self.driver.find_element(By.ID, "btnLogin").click()
        time.sleep(3)

    def extractor_venta(self):
        """Extrae los datos de la tabla para la fuerza de ventas"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "select-dropdown"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li/span[text()='14139 - GRANDES CLIENTES']"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "btnExportPOM"))).click()
        time.sleep(2)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Modal_dt_CheckOrdersPOMExportExcel_wrapper"]/div[4]/div[4]/button'))).click()
        time.sleep(2)

    def analisis_venta(self):

        pass


if __name__=="__main__":

    driver = VentaIdeal()
    driver.login_mc1()
    driver.extractor_venta()