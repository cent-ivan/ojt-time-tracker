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
- #### This app uses Python version 3.13 and above
- #### Get Package Manager: [uv](https://docs.astral.sh/uv/getting-started/installation/) 
- #### Install PostgreSQL 16.3, compiled by Visual C++ build 1939, 64-bit

## Installation
- ### Install via Docker Image
 1. Install [Docker Desktop]() first
 2. In your terminal, run the  ``` git clone https://github.com/cent-ivan/ojt-time-tracker.git```
 3. Download npm, and run the ``` npm install```, to generate your own node_modules directory
 4. Run this command to generate a tailwind file ``` npm dev run```
 5. Create a .env file (Contact how to setup)
 6. Run ```docker compose run -d db``` run db only
 7. Run ```docker compose exec backend flask db init``` (ONE PER PROJECT)
 8. Run ```docker compose exec backend flask db migrate -m "Initial schema creation"``` Defines the tables
 9. Run ```docker compose exec backend flask db upgrade``` Actually creating the table to the database
 ( . git pull          ← Code only, no containers
   . create .env       ← Create database credentials  
   . docker-compose up ← Container created with THEIR settings
 )
- ### Install via git clone.
 1. In your terminal, run the  ``` git clone https://github.com/cent-ivan/ojt-time-tracker.git```
 2. Download npm, and run the ``` npm install```, to generate your own node_modules directory
 3. Run this command to generate a tailwind file ``` npm dev run```
 4. Finally, run ` uv pip freeze -r requirements.txt` to install required python libraries.
 - Note: (This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) as a faster alternative to pip. if using pip, run `pip3 freeze -r requirements.txt`)

## Usage
- ### Running the server via Docker
 1. Runn ```docker compose up --build -d```
 2. Go to the Docker Desktop -> Containers -> In the terminal click the port 5000
 Note: (Make sure to enable Javascript)
- ### Running the server via code
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
### TEST
### GET /test
- **Description:** Tests the returned data of the methods from the repositories

## Contributing
The developer welcome contributions from the community! To get started:

1. **Fork** the repository.
2. **Clone** your fork locally:
   ```bash git clone https://github.com/cent-ivan/ojt-time-tracker.git ```
3. **Create a new branch** for your feature or fix:
   ```bash git checkout -b your-branch-name```
4. **Add and commit** your code:
   ```bash 
      git add filename
      git commit -m "short and meaningful message"
   ```
5. **Push** to your branch:
   ```bash git push origin your-branch-name```
6. **Open a Pull** Request from the main repository

## License

## Acknowledgements
