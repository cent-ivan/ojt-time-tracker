# OJT Time Tracker App

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
The OJT Time Tracker app is a personal project in which the students can keep track of their timestamp, and for the advisers to monitor students

## Features
- Automatic timestamp record
- Automatic computation of total hours and remaining hours
- Adviser dashboard for overseeing student timestamps

## Requirements and Configuration
- ### This app uses Python version 3.13 and above
- ### Get Package Manager: [uv](https://docs.astral.sh/uv/getting-started/installation/) 
- ### Install PostgreSQL 16.3, compiled by Visual C++ build 1939, 64-bit

## Installation
### Install via git clone.
 1. In your terminal, run the  ```shell git clone https://github.com/cent-ivan/ojt-time-tracker.git```
 2. Download npm, and run the ```shell npm install```
 3. Run this command to generate a tailwind file ```shell npm dev run```
 4. Finally, run ```uv pip freeze -r requirements.txt` to install required python libraries.
 Note: (This project uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/) as a faster alternative to pip. if using pip, run `pip3 freeze -r requirements.txt`)

## Usage
### Running the server
 1. Run `python run.py`
 2. Open another terrminal and run `npm run dev`
 3. Open preferred browser. Click the `http://localhost:5555` 
 Note: (Make sure to enable Javascript)

## API Endpoints
### AUTH
#### POST /adviser-login, /student-login
- **Description:** Log in a user and creates a session cookie
#### POST /adviser-signup, /student-signup
- **Description:** Creates a user and upload the data to the postgres database
### DASHBOARDS
#### GET /student-home
- **Description:** Loads the  timesheet information of the student
#### GET /adviser-home
- **Description:** Loads the list of students and their remaining time
### GET /test
- **Description:** Tests the returned data of the methods from the repositories

## Contributing

## License

## Acknowledgements
