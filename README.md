# Weather App with Redis Cache and integration with API

This app idea is taken from the roadmap.sh page and is written in **Python**

Basically I have created a CLI weather app that will fetch the city from the user input (using argparse method) and then will display temperature & feels like temp for the given city. 
The application integrates with Visual Crossing Weather API. The output is stored locally using **Redis** running inside a **Docker** container. The expiry time in the DB is set for 5 minutes (mostly for testing) 

---

## Features

* **Dynamic city selection:** Accept any city name as an argument dynamically via the terminal (currently there are no errors handling for misspelled cities - perhaps a good thing to implement in the next iteration)
* **Local data storage:** The application queries the local Redis memory cache before making any external API calls.
* **API request limitation:** If a cache hit occurs, the app skips the network request and serves the data instantly - this will save API calls and check local DB first
* **Local DB expiry :** Cached weather data expires automatically after 5 minutes (300 seconds), ensuring the user always receives up-to-date weather conditions without bloating the database. Plus it is good for testing without a need to wait e.g. 12h for the data to expire

---

## Tech Stack & Architecture

* **Python 3.x** – Core application logic.
* **Docker & Redis** – In-memory key-value database used for caching responses.
* **Requests** – HTTP library used to communicate with the Visual Crossing Weather API.
* **Argparse** – Built-in Python module for parsing command-line arguments.
* **Python-dotenv** – For managing sensitive API keys via environment variables.

---

## Installation & Setup

### 1. Clone the Repository
Clone this repository to your local machine using Git, then navigate into the project directory.


### 2. Create a virtual environment and install the required Python packages
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install requests python-dotenv redis

```

### 3. Create `.env` file in the root directory of the project and add your Visual Crossing Weather API key:

```markdown
WEATHER_API_KEY=your_actual_api_key_here
```

### 4. Ensure Docker Desktop is running on your machine, then launch the Redis container:

```markdown
docker run --name Redis_Weather_app -p 6379:6379 -d redis
```

## Usage Guide

 Run the application from your terminal by passing the city name with the `-c` or `--city` flag. If no city is specified, it defaults to Cracow.

First Execution (Cache Miss - Fetches from API & saves to Redis):

```python weather.py -c Warsaw```

Console Output:

```Data for Warsaw is NOT found in local cache! Calling API
Status code: 200
-- Pogoda for Warsaw... -- 
```
---
Second Execution (Cache Hit - Fetches instantly from Redis RAM):


```python weather.py -c Warsaw```

Console Output:

```
Data for Warsaw is found in local cache!
-- Pogoda for Warsaw... --
```

## What I have learnt 

- **I used Docker & Redis first time**  so basically I have created a Data Base
- **Using Docker and Redis** helped me understand that I don't have to call API each time, and some data can be stored locally 
- **I have built argparse app before** so this project helped my deepen my knowledge on how to implement argparse to create versatile app rather than hard-coded app that fetches only one city per call.
- **I understood the importance of `.env` file to hide API key in the project. 

