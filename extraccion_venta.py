from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pandas as pd
import json
import time


class VentaIdeal:
    """Extracción de la venta diaria"""

    def __init__(self) -> None:
        self.driver = Chrome()
        self.credenciales = self._cargar_credenciales()

    def _cargar_credenciales(self):
        with open(r"credenciales\mc1.json") as file:
            return json.load(file)

    def login_mc1(self):
        url = "https://prodweb-bimbo-las.mc1.com.br/WTM_Client/Form/Run/Custom_Check_Orders_BIMBO?menuItem=1642615056076"
        
        self.driver.get(url)
        self.driver.find_element(By.ID, "UserName").send_keys(self.credenciales["user"])
        self.driver.find_element(By.ID, "Password").send_keys(self.credenciales["password"])
        self.driver.find_element(By.ID, "Domain").send_keys(self.credenciales["domain"])
        self.driver.find_element(By.ID, "btnLogin").click()
        time.sleep(3)

    def extractor_venta(self):

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "select-dropdown"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li/span[text()='14139 - GRANDES CLIENTES']"))).click()
        self.driver.find_element(By.ID, "btnExportPOM").click()
        table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Modal_dt_CheckOrdersPOMExportExcel")))
        rows = table.find_elements(By.XPATH, "//table[@id='Modal_dt_CheckOrdersPOMExportExcel']/tbody/tr")
        headers = [header.text for header in table.find_elements(By.XPATH, "//table[@id='Modal_dt_CheckOrdersPOMExportExcel']/thead/tr/th")]

        data = []
        for row in rows:
            # Encuentra todas las celdas de la fila
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            data.append(row_data)

        return pd.DataFrame(data, columns=headers)

if __name__=="__main__":

    driver = VentaIdeal()
    driver.login_mc1()
    driver.extractor_venta().to_excel("C:\\Users\\francisco.arancibia1\\OneDrive - Corporativo Bimbo, S.A. de C. V\\Documentos\\extracciones de Python\\extractor venta.xlsx", index=False)