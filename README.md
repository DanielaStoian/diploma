# Getting Started

To get started with the application, follow these steps:

1. Navigate to the `config_dev` directory.
2. Run the following Docker Compose command to build and start the application:

docker-compose --build up


# Main Components

The primary components of this application include:

## Backend (/backend)

The backend component is implemented in Django and includes a scraping mechanism using Scrapy. It is responsible for fetching charging stations and storing them in the database. Please note that Scrapy requires a Google Maps API key to function. You should configure the API key inside the file `scrapper/stations_scrapper/stations_scrapper/spider.py` before running the scraping process.

Scrapy spiders are executed as part of the entrypoint script (`entrypoint.sh`).

## Frontend (charging-stations)

The `charging-stations` component is a React application that serves as the frontend of the application.

# Additional Files

In addition to the main components, there are several additional files and scripts that support various functionalities:

## dhmoi.py

This file contains functions for visualizing shapefiles that contain information about Greek municipalities. It also transforms shapefiles into GeoJSON format for easier use.

## dhmoi_to_cat.py

In this script, municipalities are assigned a rank (a number between 1 and 3) based on their population.

## Data Analysis (data_analysis)

Inside the `data_analysis` folder, you will find functions for generating dummy data (arrivals) for charging stations. The data is generated based on the municipality to which each station belongs.

