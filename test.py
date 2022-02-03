from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

# driver = webdriver.Edge(executable_path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


# url = "https://www.google.com.mx/?hl=es-419"
url = 'http://nts462/Reports/report/Cimplicity_Reports/Traceablity_Reports/Process%20Traceability'
driver = webdriver.Edge(executable_path="msedgedriver.exe")
driver.maximize_window()
driver.get(url)



# inputElement = driver.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/div[2]/div/table/tbody/tr[2]/td/div/div/table/tbody/tr/td[1]/table/tbody/tr[3]/td[5]/div/table/tbody/tr/td/input")


inputElement = driver.find_elements(By.TAG_NAME, "paginated-report-viewer")

# inputElement = inputElement.switch_to_frame(0)
# tag_name
# asd = inputElement.find_element_by_xpath("//*[@id='ReportViewerControl_ctl04_ctl13_txtValue']")
# inputElement = driver.find_element(By.ID, "portal")
# inputElement = inputElement.find_element(By.XPATH, "/body")

if isinstance(inputElement, list):

    print("this is the len: ", len(inputElement))
    for elm in inputElement:
        print("Element: ", elm.tag_name)

else:
    print(inputElement.tag_name)
# inputElement.send_keys("GE54055D01CM1110010121E2102111190021")
# print(inputElement.tag_name)
print("\n\n\n")
print(driver.page_source)