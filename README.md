# Crypto and Stock Sentiment Analysis via Twitter

## Project Overview
This project leverages the Twitter API to gather and analyze sentiments around cryptocurrencies and stocks by collecting tweets with specific keywords. It stores the fetched data in a PostgreSQL database hosted on Heroku for subsequent analysis.

## Features
- **Data Collection**: Automated collection of tweets using the Twitter API, filtered by keywords related to cryptocurrencies and stocks.
- **Database Storage**: Efficient storage of tweet data in a Heroku PostgreSQL database, designed to prevent data duplication and facilitate accessible analysis.
- **Expandability**: Flexibility to include additional keywords or extend analysis to other market segments.

## Getting Started

### Prerequisites
Before running the project, ensure you have the following:
- Python 3.8 or newer installed on your system.
- Tweepy, pandas, SQLAlchemy, and psycopg2 libraries installed. These can be installed via pip using the provided `requirements.txt`.

### Setup Instructions
1. **Clone the Repository**
2. **Twitter API Credentials**: Obtain your credentials by setting up a Twitter Developer account and creating an app. Store your credentials in a twitter_keys.py file.
3. **Database Configuration**: Configure your PostgreSQL database on Heroku and update the engine variable in the script with your connection details.

##Contributing
We welcome contributions to this project. If you have suggestions for improvements or want to add new features, please fork the repository, make your changes, and submit a pull request.

#Disclaimer
This project is intended for educational and research purposes only. Users must comply with the Twitter API terms of service.

##Acknowledgments
Twitter, for providing the API that enables this project.
The open-source community, for the libraries that facilitate this analysis.
