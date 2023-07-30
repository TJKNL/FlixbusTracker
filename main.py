from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import threading

app = Flask(__name__)

status_bus1 = ""
status_bus2 = ""

def fetch_bus_status(url):
    options = Options()
    options.add_argument("--headless")  # Uncomment this line if you want Firefox to run in headless mode
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(3)  # wait for the JavaScript to run and the page to load
    status_element = driver.find_element(By.CLASS_NAME, 'hcr-tag__text')
    status = status_element.text if status_element else "Status not found"
    driver.quit()
    return status

def update_status():
    global status_bus1, status_bus2
    url_bus1 = 'https://global.flixbus.com/track/ride/d6b01d05-5b15-4d45-8c35-1404fc7c83d9?fromStopUuid=dcbd0b4b-9603-11e6-9066-549f350fcb0c&toStopUuid=dcbabf60-9603-11e6-9066-549f350fcb0c'  # replace with actual URL
    url_bus2 = 'https://global.flixbus.com/track/ride/3a0b21d8-acc4-4f3e-a04e-35d419a02e4f?fromStopUuid=dcbb7621-9603-11e6-9066-549f350fcb0c&toStopUuid=dcbdd1b1-9603-11e6-9066-549f350fcb0c'  # replace with actual URL
    while True:
        status_bus1 = fetch_bus_status(url_bus1)
        status_bus2 = fetch_bus_status(url_bus2)
        time.sleep(60)  # update status every minute

@app.route('/')
def home():
    return render_template('index.html', status_bus1=status_bus1, status_bus2=status_bus2)

if __name__ == '__main__':
    status_thread = threading.Thread(target=update_status)
    status_thread.start()
    app.run(host='192.168.1.10', port=5000, debug=True)  # specify IP and port here