from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Запуск веб-драйвера (вам может потребоваться указать путь к драйверу)
driver = webdriver.Chrome()

# Открытие веб-страницы
driver.get("https://matrixcalc.org/slu.html")

# Ожидание загрузки страницы
time.sleep(5    )
# Находим все кнопки с классом "swap-mode-button" (кнопки "Cells")
buttons = driver.find_elements(By.CLASS_NAME, "swap-mode-button")
print(buttons)
for i in range(1):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swap-mode-button")))
    buttons[i].click()

# Вставляем текст в поля
textarea = driver.find_element(By.CLASS_NAME,"matrix-table-textarea")
text ="-2 2 -3\n -1 1 3"  # Ваш текст для вставки
textarea.clear()  
textarea.send_keys(text)  

# # Закрываем браузер
time.sleep(15)
driver.quit()