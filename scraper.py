import time
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from flask import Flask, render_template_string
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Import credentials
from credentials import (
    TWITTER_USERNAME, TWITTER_PASSWORD, MONGODB_URI, 
    PROXYMESH_USERNAME, PROXYMESH_PASSWORD, PROXYMESH_HOST
)

# Selenium WebDriver setup
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--proxy-server=http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{PROXYMESH_HOST}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Scrape trending topics
def scrape_trending_topics():
    driver = setup_driver()
    driver.get("https://twitter.com/i/flow/login")
    time.sleep(3)

    # Login to Twitter
    driver.find_element(By.NAME, "text").send_keys(TWITTER_USERNAME, Keys.RETURN)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(TWITTER_PASSWORD, Keys.RETURN)
    time.sleep(5)

    # Click on "Explore"
    explore_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="AppTabBar_Explore_Link"]'))
    )
    explore_button.click()

    # Navigate to "Trending" tab
    trending_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/explore/tabs/trending"]'))
    )
    trending_tab.click()

    # Fetch trending topics
    trends = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]'))
    )
    trending_topics = [trend.text for trend in trends[:5]]  # Top 5 trends

    # Get proxy IP address
    driver.get("https://api.ipify.org")
    ip_address = driver.find_element(By.TAG_NAME, "body").text

    driver.quit()
    return trending_topics, ip_address


def store_in_mongodb(trends, ip_address):
    client = MongoClient(MONGODB_URI)
    db = client["twitter_trends"]
    collection = db["trending"]
    record = {
        "_id": str(uuid.uuid4()),
        "trends": trends,
        "timestamp": datetime.now(),
        "ip_address": ip_address,
    }
    collection.insert_one(record)
    client.close()
    return record

# Flask app for frontend
app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Twitter Trends</h1>
        <button onclick="window.location.href='/run'">Click here to run the script</button>
    </body>
    </html>
    ''')


@app.route("/run")
def run_script():
    trends, ip_address = scrape_trending_topics()
    record = store_in_mongodb(trends, ip_address)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>These are the most happening topics as on {{ record['timestamp'] }}</h1>
        <ul>
            {% for trend in record['trends'] %}
                <li>{{ trend }}</li>
            {% endfor %}
        </ul>
        <p>The IP address used for this query was {{ record['ip_address'] }}</p>
        <button onclick="window.location.href='/run'">Click here to run the query again</button>
    </body>
    </html>
    ''', record=record)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
