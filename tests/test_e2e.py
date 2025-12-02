import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost:5002"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

def test_full_flow(driver):
    driver.get(f"{BASE_URL}/register")
    
    timestamp = int(time.time())
    username = f"e2e_{timestamp}"
    
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm").send_keys("password")
    driver.find_element(By.TAG_NAME, "button").click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("login"))
    
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "button").click()
    
    try:
        WebDriverWait(driver, 10).until(EC.url_to_be(f"{BASE_URL}/"))
    except:
        print("Failed to redirect to index. Current URL:", driver.current_url)
        print("Page Source:", driver.page_source)
        raise
    
    if f"Logged in as {username}" not in driver.page_source:
        print("Login verification failed. Page Source:", driver.page_source)
    assert f"Logged in as {username}" in driver.page_source
    
    driver.find_element(By.LINK_TEXT, "New Task").click()
    
    driver.find_element(By.NAME, "title").send_keys("Selenium Task")
    driver.find_element(By.NAME, "description").send_keys("Created via E2E test")
    
    date_input = driver.find_element(By.NAME, "due_date")
    driver.execute_script("arguments[0].value = '2025-12-31';", date_input)
    
    driver.find_element(By.TAG_NAME, "button").click()
    
    try:
        WebDriverWait(driver, 10).until(EC.url_to_be(f"{BASE_URL}/"))
    except:
        print("Failed to redirect to index after task creation. Current URL:", driver.current_url)
        print("Page Source:", driver.page_source)
        raise
    
    assert "Selenium Task" in driver.page_source

    
    complete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete')]"))
    )
    complete_btn.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Reopen')]"))
    )
    
    delete_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Delete')]")
    delete_btn.click()
    
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        print("No alert found or auto-accepted")
        
    time.sleep(1)
    
    assert "Selenium Task" not in driver.page_source
