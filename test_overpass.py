import requests

url = "https://overpass-api.de/api/interpreter"
lat, lon = 28.7041, 77.1025

query = f"""
[out:json];
node
  ["amenity"="hospital"]
  (around:3000,{lat},{lon});
out;
"""

print("Running WITHOUT headers...")
response = requests.post(url, data=query, timeout=15)
print("Status:", response.status_code)
if response.status_code != 200:
    print("Response:", response.text)

print("\nRunning WITH headers...")
headers = {
    "User-Agent": "HospitalLocatorApp/1.0 (contact: test@example.com)",
    "Accept": "*/*"
}
response = requests.post(url, data=query, headers=headers, timeout=15)
print("Status:", response.status_code)
if response.status_code != 200:
    print("Response:", response.text)
