from flask import Flask, render_template, request, jsonify
import requests
import math
import heapq
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

app = Flask(__name__)

# 🔑 OpenAI (optional)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Distance Calculation
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.asin(math.sqrt(a))
    return R * c


# -----------------------------
# FETCH HOSPITALS (WITH CATEGORY)
# -----------------------------
def fetch_hospitals(lat, lon, category=None):
    url = "https://overpass-api.de/api/interpreter"

    # ✅ CATEGORY LOGIC
    if category == "maternity":
        tag = '["healthcare"="maternity"]'
    elif category == "dentist":
        tag = '["amenity"="dentist"]'
    elif category == "cardiology":
        tag = '["healthcare:speciality"="cardiology"]'
    elif category == "pediatric":
        tag = '["healthcare:speciality"="pediatrics"]'
    elif category == "neurology":
        tag = '["healthcare:speciality"="neurology"]'
    elif category == "psychology":
       tag = '["healthcare:speciality"="psychology"]'
    elif category == "orthopedic":
       tag = '["healthcare:speciality"="orthopaedics"]'
    elif category == "emergency":
       tag = '["emergency"="yes"]'
    else:
        tag = '["amenity"="hospital"]'
    

    # ✅ QUERY
    query = f"""
[out:json];
node{tag}({lat-0.05},{lon-0.05},{lat+0.05},{lon+0.05});
out;
"""

    headers = {
        "User-Agent": "HospitalLocatorApp/1.0",
        "Accept": "*/*"
    }

    try:
        response = requests.post(url, data=query, headers=headers, timeout=15)

        if response.status_code != 200:
            print("❌ Overpass Error:", response.status_code)
            print(response.text)
            return []

        data = response.json()

        hospitals = data.get("elements", [])
        print(f"✅ Hospitals fetched ({category}):", len(hospitals))

        return hospitals

    except Exception as e:
        print("❌ Exception:", e)
        return []


# -----------------------------
# DIJKSTRA (PRIORITY QUEUE)
# -----------------------------
def dijkstra(user_lat, user_lon, hospitals):
    pq = []
    result = []

    for hospital in hospitals:
        if "lat" not in hospital or "lon" not in hospital:
            continue

        dist = haversine(user_lat, user_lon, hospital["lat"], hospital["lon"])
        heapq.heappush(pq, (dist, hospital))

    while pq:
        dist, hospital = heapq.heappop(pq)

        result.append({
            "name": hospital.get("tags", {}).get("name", "Unnamed Hospital"),
            "lat": hospital["lat"],
            "lon": hospital["lon"],
            "distance": round(dist, 2)
        })

    return result


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find-hospital", methods=["POST"])
def find_hospital():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"hospitals": [], "best_hospital": None})

        user_lat = data.get("lat")
        user_lon = data.get("lon")
        category = data.get("category")  # ✅ NEW

        if user_lat is None or user_lon is None:
            return jsonify({"hospitals": [], "best_hospital": None})

        hospitals = fetch_hospitals(user_lat, user_lon, category)

        # ❗ fallback if no results
        if not hospitals:
            print("⚠️ No results for category, fallback to general hospitals")
            hospitals = fetch_hospitals(user_lat, user_lon, None)

        if not hospitals:
            return jsonify({
                "hospitals": [],
                "best_hospital": None,
                "error": "No hospitals found."
            })

        sorted_hospitals = dijkstra(user_lat, user_lon, hospitals)

        best = sorted_hospitals[0] if sorted_hospitals else None

        return jsonify({
            "hospitals": sorted_hospitals,
            "best_hospital": best
        })

    except Exception as e:
        print("❌ SERVER ERROR:", e)

        return jsonify({
            "hospitals": [],
            "best_hospital": None,
            "error": str(e)
        })


# -----------------------------
# CHATBOT (OPTIONAL)
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
Respond ONLY in JSON:
{
  "reply": "...",
  "intent": "FIND_HOSPITAL or EMERGENCY or NONE"
}
"""
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(content)
        except:
            parsed = {
                "reply": "I can help you find hospitals.",
                "intent": "NONE"
            }

        return jsonify(parsed)

    except Exception as e:
        print("❌ CHAT ERROR:", e)

        return jsonify({
            "reply": "AI not working right now.",
            "intent": "NONE"
        })


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)