# Automated ETL & Data Visualization Pipeline Project #
  <img width="1000" height="720" alt="Gemini_Generated_Image_bd2hawbd2hawbd2h" src="https://github.com/user-attachments/assets/2d7a8135-871b-4579-8a07-3e2569f122b8" />

**Introduction:**

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline for automated data collection from a website, storage in a database, and later visualize the results. It serves as a case study for fundamental data management skills.

## Extract (Web Scraping):

<img width="1024" height="480" alt="inspection" src="https://github.com/user-attachments/assets/8c347676-ae3a-4fb6-8433-ef9711d30abd" />

The extraction phase uses web scraping to collect financial data from an external website. Instead of a public API, the data points for gold and Bitcoin prices were directly extracted from the site's source code. 
The relevant data was identified by manually inspecting the network traffic using a browser's developer tools (in the Fetch/XHR section). This enabled a direct approach to fetching the data URL.

*Responsibility: this website does not had any `/robots.txt` instruction for bots/crawlers, and I scheduled an extraction for only every 30 min not to put too much extra load to the site.* 


## Transform:

<img width="700" height="277" alt="json data" src="https://github.com/user-attachments/assets/034bbf99-9988-4c76-b9a2-2535914f3344" />

After extraction, the raw data is transformed into a structured format for database preparation. The Python requests module is used to retrieve the raw JSON data.
The JSON response is processed to isolate only the relevant fields: the asset name (name) and its price (price) separately a timestamp (created_at) with the time of extraction is also added.

## Load:

The cleaned up data is loaded into a MariaDB database which serves as the data repository to create a historical record that can be used for analysis and visualization. 
The data is stored in the "assets" table, which is created using the following SQL statement:

    CREATE TABLE assets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

## Automation:

<img width="480" height="480" alt="x2go" src="https://github.com/user-attachments/assets/2a90c8a2-7f18-476e-8dfe-b24c696ffc68" />

The pipeline is deployed for continuous, automated execution. The Python script is run on a Raspberry Pi using a Cron job. 
(The Pi was controlled either headless with terminal SSH commands, or through x2Go client via a Linux Mint based PC) 

The following Cron-job entry ensures an automatic run every 30 minutes:

    */30 * * * * python3 /path/to/scraper.py


## Visualization:

A separate PHP file serves as a web frontend that calls the Python script to generate the interactive graph with the help of the Plotly module.

<img width="1000" height="720" alt="Screenshot at 2025-09-30 20-37-53" src="https://github.com/user-attachments/assets/a041de82-5f8b-4b0d-8a9e-4e6da5bdc27e" />

For testing purposes I was using PHPs own built-in server with the following command:

    $ php -S localhost:8000

