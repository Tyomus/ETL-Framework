import requests
import mysql.connector

DB_HOST = "localhost"
DB_USER = "scraper"
DB_PASSWORD = ""
DB_NAME = "etl_project"

URLS = [
    "https://api.gold-api.com/price/XAU",
    "https://api.gold-api.com/price/BTC"
]

def fetch_and_clean_data():
    all_cleaned_data = []

    for url in URLS:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            cleaned_data = {
                "name": data.get("name"),
                "price": data.get("price")
            }
            all_cleaned_data.append(cleaned_data)
        
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching data from {url}: {e}")
            pass

    return all_cleaned_data

def insert_data_into_db(data):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        sql = "INSERT INTO assets (name, price) VALUES (%s, %s)"

        for row in data:
            name = row.get("name")
            price = row.get("price")
            
            if name and price:
                cursor.execute(sql, (name, price))

        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        pass
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    cleaned_data = fetch_and_clean_data()
    if cleaned_data:
        insert_data_into_db(cleaned_data)