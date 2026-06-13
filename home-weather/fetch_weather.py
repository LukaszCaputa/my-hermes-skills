#!/usr/bin/env python3
"""
Fetch current weather data from Weather Underground PWS dashboard.
Target: https://www.wunderground.com/dashboard/pws/IWARSA513

The page embeds JSON data in a <script id="app-root-state"> tag.
This script extracts the most recent PWS observation and converts
imperial units to metric (Celsius, hPa).
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import sys
from datetime import datetime


STATION_ID = "IWARSA513"
URL = f"https://www.wunderground.com/dashboard/pws/{STATION_ID}"

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def fahrenheit_to_celsius(f):
    """Convert Fahrenheit to Celsius."""
    return round((f - 32) * 5.0 / 9.0, 1)


def inhg_to_hpa(inhg):
    """Convert inches of mercury to hectopascals."""
    return round(inhg * 33.8639, 2)


def mph_to_kmh(mph):
    """Convert miles per hour to kilometers per hour."""
    return round(mph * 1.60934, 1)


def fetch_weather_data():
    """Fetch and parse current weather data from Weather Underground PWS dashboard."""

    try:
        print(f"Fetching data from: {URL}")
        response = requests.get(URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        print(f"Response status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    # Parse the HTML to find the embedded JSON state
    soup = BeautifulSoup(response.text, 'html.parser')
    state_script = soup.find('script', id='app-root-state')

    if not state_script:
        print("Error: Could not find embedded JSON state in page.")
        return None

    script_content = state_script.string
    if not script_content:
        print("Error: Embedded JSON state script is empty.")
        return None

    try:
        state_data = json.loads(script_content)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing embedded JSON: {e}")
        return None

    # Find the key containing PWS observations data
    # The URL pattern is: /v2/pws/observations/all/1day
    observations = None
    for key, value in state_data.items():
        if isinstance(value, dict) and 'u' in value:
            url = value.get('u', '')
            if 'pws/observations' in url:
                body = value.get('b', {})
                if isinstance(body, dict) and 'observations' in body:
                    observations = body['observations']
                    break

    if not observations:
        print("Error: Could not find PWS observations data in page state.")
        return None

    # Get the most recent observation (last in the array)
    latest = observations[-1]

    # Extract imperial values
    imperial = latest.get('imperial', {})

    temp_f = imperial.get('tempAvg')
    humidity = latest.get('humidityAvg')
    pressure_inhg = imperial.get('pressureMax')
    windspeed_mph = imperial.get('windspeedAvg')
    windgust_mph = imperial.get('windgustAvg')
    winddir = latest.get('winddirAvg')
    dewpoint_f = imperial.get('dewptAvg')
    obs_time_local = latest.get('obsTimeLocal', 'N/A')

    # Convert to metric
    temp_c = fahrenheit_to_celsius(temp_f) if temp_f is not None else None
    dewpoint_c = fahrenheit_to_celsius(dewpoint_f) if dewpoint_f is not None else None
    pressure_hpa = inhg_to_hpa(pressure_inhg) if pressure_inhg is not None else None
    windspeed_kmh = mph_to_kmh(windspeed_mph) if windspeed_mph is not None else None
    windgust_kmh = mph_to_kmh(windgust_mph) if windgust_mph is not None else None

    # Build result
    weather_data = {
        'station_id': STATION_ID,
        'observation_time_local': obs_time_local,
        'temperature_c': temp_c,
        'humidity_pct': humidity,
        'pressure_hpa': pressure_hpa,
        'dewpoint_c': dewpoint_c,
        'wind_speed_kmh': windspeed_kmh,
        'wind_gust_kmh': windgust_kmh,
        'wind_direction_deg': winddir,
        'fetched_at': datetime.now().isoformat(),
    }

    # Print results
    print()
    print("=" * 55)
    print(f"  Weather Data for {STATION_ID} (Warsaw)")
    print("=" * 55)
    print(f"  Observation time : {obs_time_local}")
    print(f"  Temperature      : {temp_c} C" if temp_c is not None else "  Temperature      : N/A")
    print(f"  Humidity         : {humidity}%" if humidity is not None else "  Humidity         : N/A")
    print(f"  Pressure         : {pressure_hpa} hPa" if pressure_hpa is not None else "  Pressure         : N/A")
    print(f"  Dewpoint         : {dewpoint_c} C" if dewpoint_c is not None else "  Dewpoint         : N/A")
    print(f"  Wind speed       : {windspeed_kmh} km/h" if windspeed_kmh is not None else "  Wind speed       : N/A")
    print(f"  Wind gust        : {windgust_kmh} km/h" if windgust_kmh is not None else "  Wind gust        : N/A")
    print(f"  Wind direction   : {winddir} deg" if winddir is not None else "  Wind direction   : N/A")
    print("=" * 55)

    # Save to JSON
    output_file = 'weather_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2, ensure_ascii=False)
    print(f"\nData saved to: {output_file}")

    return weather_data


if __name__ == "__main__":
    result = fetch_weather_data()
    if result:
        print("\n[OK] Successfully fetched weather data")
    else:
        print("\n[FAIL] Failed to fetch weather data")
        sys.exit(1)
