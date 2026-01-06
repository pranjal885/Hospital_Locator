from flask import Flask, render_template, request, jsonify
import requests
import math

app = Flask(__name__)

# -----------------------------
# Distance Calculation (DSA LOGIC)
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.asin(math.sqrt(a))
    return R * c


# -----------------------------
# Fetch hospitals using OSM API
# -----------------------------
def fetch_hospitals(lat, lon):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    node
      ["amenity"="hospital"]
      (around:5000,{lat},{lon});
    out;
    """

    response = requests.post(url, data=query)
    return response.json()["elements"]



# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find-hospital", methods=["POST"])
def find_hospital():
    data = request.json
    user_lat = data["lat"]
    user_lon = data["lon"]

    hospitals = fetch_hospitals(user_lat, user_lon)

    hospital_list = []

    for hospital in hospitals:
        h_lat = hospital["lat"]
        h_lon = hospital["lon"]

        dist = haversine(user_lat, user_lon, h_lat, h_lon)

        hospital_list.append({
            "name": hospital.get("tags", {}).get("name", "Unnamed Hospital"),
            "lat": h_lat,
            "lon": h_lon,
            "distance": round(dist, 2)
        })

    # 🔥 DSA PART: sort hospitals by distance
    hospital_list.sort(key=lambda x: x["distance"])

    return jsonify(hospital_list)



import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

