---
name: home-weather
description: "Fetch current weather data from Weather Underground PWS dashboard for home location (Warsaw, station IWARSA513). Activated by Polish trigger phrases."
version: 1.0.0
author: [lukasz-caputa]
license: MIT
platforms: [linux, macos, windows]
compatibility: "Requires Python 3.7+ and internet access to wunderground.com"
prerequisites:
  commands: ["python3"]
  python_packages: ["requests", "bs4"]
setup:
  help: "Run 'pip install requests bs4' or 'pip3 install requests bs4' to install required Python packages before first use."
metadata:
  hermes:
    tags:
      - weather
      - home-automation
      - pws
      - wunderground
      - polish
    related_skills: []
    category: utility
    triggers:
      - "pogoda w domu"
      - "pogoda jaracza"
      - "pogoda balkon"
---

# Home Weather

Fetch current weather data from Weather Underground Personal Weather Station (PWS) dashboard for home location in Warsaw (station ID: IWARSA513).

## What's in this skill

**Script:**

| Script | Purpose |
|--------|---------|
| `fetch_weather.py` | Fetches and parses current weather data from Weather Underground PWS dashboard, converts imperial units to metric (Celsius, hPa, km/h), and saves results to `weather_data.json` |

## When to Use

This skill is activated when the user says any of the following Polish phrases:

- **"pogoda w domu"** (weather at home)
- **"pogoda jaracza"** (weather at Jaracza street)
- **"pogoda balkon"** (balcony weather)

Use this skill when:
- User asks for current weather conditions at home
- User wants to check temperature, humidity, pressure, or wind data from the home weather station
- User needs real-time PWS (Personal Weather Station) data

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ Weather Underground PWS Dashboard                   │
│ https://www.wunderground.com/dashboard/pws/IWARSA513│
└─────────────────────────┬───────────────────────────┘
                          │
                          │ HTTP GET (scraping)
                          │
┌─────────────────────────▼───────────────────────────┐
│ fetch_weather.py                                    │
│ - Fetches HTML page                                 │
│ - Extracts embedded JSON from <script> tag          │
│ - Parses PWS observations                           │
│ - Converts imperial → metric units                  │
│ - Saves to weather_data.json                        │
└─────────────────────────────────────────────────────┘
```

## Quick Start

### Step 1: Install Python dependencies (FIRST TIME ONLY)

Before running the skill for the first time, install the required Python packages:

```bash
pip install requests bs4
# Or if using pip3:
pip3 install requests bs4
# Or with python -m pip:
python3 -m pip install requests bs4
```

### Step 2: Fetch weather data

```bash
python3 fetch_weather.py
```

The script will:
1. Fetch the PWS dashboard page from Weather Underground
2. Extract the embedded JSON state containing weather observations
3. Parse the most recent observation data
4. Convert imperial units to metric (Celsius, hPa, km/h)
5. Display formatted weather data to stdout
6. Save the data to `weather_data.json`

### Step 3: Read the results

The script outputs formatted weather data:

```
=======================================================
  Weather Data for IWARSA513 (Warsaw)
=======================================================
  Observation time : 2026-06-13 15:30:00
  Temperature      : 22.5 C
  Humidity         : 65%
  Pressure         : 1013.25 hPa
  Dewpoint         : 15.3 C
  Wind speed       : 12.5 km/h
  Wind gust        : 18.2 km/h
  Wind direction   : 225 deg
=======================================================
```

The data is also saved to `weather_data.json` in JSON format:

```json
{
  "station_id": "IWARSA513",
  "observation_time_local": "2026-06-13 15:30:00",
  "temperature_c": 22.5,
  "humidity_pct": 65,
  "pressure_hpa": 1013.25,
  "dewpoint_c": 15.3,
  "wind_speed_kmh": 12.5,
  "wind_gust_kmh": 18.2,
  "wind_direction_deg": 225,
  "fetched_at": "2026-06-13T15:30:45.123456"
}
```

## Core Workflow

### Trigger Detection

When the user says any of the trigger phrases ("pogoda w domu", "pogoda jaracza", "pogoda balkon"), the agent should:

1. **Check if dependencies are installed:**
   ```bash
   python3 -c "import requests; import bs4; print('OK')"
   ```
   If this fails, run the setup command first.

2. **Execute the weather script:**
   ```bash
   python3 fetch_weather.py
   ```

3. **Parse the output:**
   - Read the formatted weather data from stdout
   - Or read the `weather_data.json` file for structured data

4. **Present the results to the user:**
   - Summarize the current weather conditions
   - Highlight key metrics (temperature, humidity, wind)
   - Mention the observation time

### Error Handling

The script handles common errors:

- **Network errors:** "Error fetching data: [error message]"
- **Missing data:** "Error: Could not find embedded JSON state in page"
- **Parse errors:** "Error parsing embedded JSON: [error message]"

If the script fails, check:
- Internet connectivity to wunderground.com
- Whether the PWS station IWARSA513 is online
- Whether the page structure has changed (may require script updates)

## Decision Tree

| User says | Action |
|-----------|--------|
| "pogoda w domu" | Run `python3 fetch_weather.py` and present results |
| "pogoda jaracza" | Run `python3 fetch_weather.py` and present results |
| "pogoda balkon" | Run `python3 fetch_weather.py` and present results |
| "what's the weather at home?" | Run `python3 fetch_weather.py` and present results |
| "check home weather station" | Run `python3 fetch_weather.py` and present results |

## Setup & Onboarding

### First-Time Setup

Before using the skill, install the required Python packages:

```bash
# Option 1: Using pip
pip install requests bs4

# Option 2: Using pip3
pip3 install requests bs4

# Option 3: Using python -m pip
python3 -m pip install requests bs4

# Option 4: Using a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install requests bs4
```

### Verification

After installation, verify the packages are available:

```bash
python3 -c "import requests; import bs4; print('Dependencies OK')"
```

If this prints "Dependencies OK", the skill is ready to use.

## Data Fields

The weather data includes the following metrics:

| Field | Unit | Description |
|-------|------|-------------|
| `station_id` | - | Weather Underground PWS station ID (IWARSA513) |
| `observation_time_local` | - | Local time of the observation |
| `temperature_c` | °C | Temperature in Celsius |
| `humidity_pct` | % | Relative humidity percentage |
| `pressure_hpa` | hPa | Atmospheric pressure in hectopascals |
| `dewpoint_c` | °C | Dew point temperature in Celsius |
| `wind_speed_kmh` | km/h | Average wind speed in kilometers per hour |
| `wind_gust_kmh` | km/h | Wind gust speed in kilometers per hour |
| `wind_direction_deg` | degrees | Wind direction in degrees (0-360) |
| `fetched_at` | ISO 8601 | Timestamp when the data was fetched |

## Pitfalls

1. **Dependencies must be installed first** — The script requires `requests` and `bs4` (BeautifulSoup4) Python packages. Without them, the script will fail with `ModuleNotFoundError`.

2. **Internet connection required** — The script fetches data from wunderground.com, so an active internet connection is necessary.

3. **PWS station must be online** — If the personal weather station IWARSA513 is offline or not reporting data, the script may return stale or missing observations.

4. **Rate limiting** — Weather Underground may rate-limit requests. Avoid running the script too frequently (e.g., more than once per minute).

5. **Page structure changes** — Weather Underground may change their page structure, which could break the scraping logic. If the script fails with "Could not find embedded JSON state", the page structure may have changed.

6. **Unit conversions** — The script automatically converts imperial units (Fahrenheit, inches of mercury, mph) to metric (Celsius, hPa, km/h). The raw data from Weather Underground is in imperial units.

7. **Data freshness** — The observation time indicates when the data was recorded by the PWS, not when it was fetched. Check the `observation_time_local` field to ensure the data is current.

## Example Usage

### Example 1: Basic weather check

**User:** "pogoda w domu"

**Agent:**
```bash
python3 fetch_weather.py
```

**Output:**
```
Fetching data from: https://www.wunderground.com/dashboard/pws/IWARSA513
Response status: 200

=======================================================
  Weather Data for IWARSA513 (Warsaw)
=======================================================
  Observation time : 2026-06-13 15:30:00
  Temperature      : 22.5 C
  Humidity         : 65%
  Pressure         : 1013.25 hPa
  Dewpoint         : 15.3 C
  Wind speed       : 12.5 km/h
  Wind gust        : 18.2 km/h
  Wind direction   : 225 deg
=======================================================

Data saved to: weather_data.json

[OK] Successfully fetched weather data
```

**Agent response to user:**
"Aktualna pogoda w domu (stacja IWARSA513):
- Temperatura: 22.5°C
- Wilgotność: 65%
- Ciśnienie: 1013.25 hPa
- Prędkość wiatru: 12.5 km/h
- Kierunek wiatru: 225° (południowy zachód)
- Czas pomiaru: 2026-06-13 15:30:00"

### Example 2: Checking balcony conditions

**User:** "pogoda balkon"

**Agent:** Runs the script and focuses on wind and temperature data relevant for balcony conditions.

**Agent response:**
"Warunki na balkonie:
- Temperatura: 22.5°C
- Wiatr: 12.5 km/h z południowego zachodu
- Porywy wiatru: 18.2 km/h
- Wilgotność: 65%"

## Verification Checklist

Before using the skill, ensure:

- [ ] Python 3.7+ is installed
- [ ] `requests` package is installed (`python3 -c "import requests"`)
- [ ] `bs4` package is installed (`python3 -c "import bs4"`)
- [ ] Internet connection is available
- [ ] The `fetch_weather.py` script exists in the workspace
- [ ] The script can successfully fetch data (run once to verify)
