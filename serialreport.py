from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# serial = "GE54055D01CM1110010121E2102111190021"

def show(serial:str = ''):

    url = 'http://nts462/Reports/report/Cimplicity_Reports/Traceablity_Reports/Process%20Traceability'


    driver = webdriver.Edge(executable_path=r'msedgedriver.exe')
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    try:
        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/section[2]/div/paginated-report-viewer/div/div/div[1]/iframe")))
        time.sleep(1)
    finally:
        # print(driver.page_source)
        viewer_frame = driver.find_element(By.CLASS_NAME, "viewer")
        driver.switch_to.frame(viewer_frame)

        serial_input = driver.find_element(By.ID, "ReportViewerControl_ctl04_ctl13_txtValue")
        serial_input.send_keys(serial)

        view_report_button = driver.find_element(By.ID, "ReportViewerControl_ctl04_ctl00")
        view_report_button.click()
    
    
    while True:
        try:
            _ = driver.window_handles
        except Exception as e:
            # print("pringaoopp-------------------")
            break
        time.sleep(0.1)




# show(serial)