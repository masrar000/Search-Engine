# InquireNet Search Engine

InquireNet is a simple and visually appealing web-based search engine that allows users to perform searches across multiple search engines including Google, Bing, Yahoo, and DuckDuckGo. It features a responsive front-end, advanced web scraping, and data storage capabilities.

# Features

Responsive Front-End: Developed with HTML and CSS for a user-friendly experience.

Multi-Engine Search: Supports searching through Google, Bing, Yahoo, and DuckDuckGo.

Data Storage: Uses MySQL/PostgreSQL for storing search terms and results.

ETL Process: Automated data ingestion to extract, transform, and load search results.

Frequency Analysis: Ranks and displays search results based on term frequency.

# Installation

To install and run InquireNet locally, follow these steps:

Prerequisites
Python 3.x
MySQL or PostgreSQL
pip (Python package installer)

## Steps

1. Clone the Repository

Copy code
git clone https://github.com/masrar000/Search-Engine.git
cd Search-Engine

2. Create a Virtual Environment


Copy code

python -m venv venv

source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. Install Dependencies

Copy code

pip install -r requirements.txt

4. Database Setup

Create a new database in MySQL or PostgreSQL.

Update the database configuration in the Python scripts to connect to your database.

5. Run the Application

Copy code

python websearch.py

6. Access the Application

Open your web browser and navigate to http://127.0.0.1:5000.

# Usage

Home Page: Enter your search query in the search box and click "Search".

Results Page: View the search results ranked by term frequency. Click on any result to visit the respective page.

# File Structure

websearch.html: Landing page for entering search queries.

results.html: Displays the search results.

style.css: Stylesheet for the HTML pages.

websearch.py: Main application script.

pagerank.py: Script for ranking search results.

search_terms.py: Script for handling search terms.

web_spider.py: Web scraping script.

crawled_pages.db: Database file for storing crawled pages.

# Contributing
Contributions are welcome! Please create a pull request or submit an issue for any improvements or bug fixes.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements

Flask

BeautifulSoup

requests
