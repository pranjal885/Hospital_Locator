# 🏥 Smart Hospital Finder
A smart location-based web application that helps users quickly find the nearest relevant healthcare facilities based on their needs, with real-time routing and navigation support.

## 🔗 Live Demo : https://hospital-locator-f460.onrender.com/

## 🚀 Features

- 📍 Automatic Location Detection (Geolocation API)
- 🏥 Category-Based Search:
  - General Hospitals  
  - Maternity  
  - Dentist  
  - Cardiologist  
  - Pediatrician  
  - Neurologist  
  - Psychologist  
  - Orthopedic  
  - Emergency (Accident)  
- 📊 Nearest Hospital Ranking using DSA (Priority Queue)
- 🗺️ Interactive Map using Leaflet.js
- 🚗 Route Visualization
- 🌐 Google Maps Navigation Integration
- 🎨 Clean and responsive UI

## 🧠 How It Works

1. User selects a hospital category  
2. Browser fetches user's current location  
3. Frontend sends location + category to backend  
4. Backend queries OpenStreetMap (Overpass API)  
5. Hospitals are filtered based on category  
6. Distance is calculated using Haversine formula  
7. Hospitals are sorted using Priority Queue (Min Heap)  
8. Results are displayed on map and list  
9. User can navigate using Google Maps  

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet.js

### Backend
- Python
- Flask

### APIs Used
- OpenStreetMap (Overpass API)
- Geolocation API
- Google Maps Navigation

## ⚙️ Setup Instructions

1. Clone the repository:
   git clone https://github.com/your-username/Hospital_Locator.git

2. Navigate to project folder:
   cd Hospital_Locator

3. Create virtual environment:
   python -m venv venv

4. Activate environment:
   venv\Scripts\activate   (Windows)

5. Install dependencies:
   pip install -r requirements.txt

6. Create `.env` file and add:
   OPENAI_API_KEY=your_api_key

7. Run the app:
   python app.py

8. Open browser:
   http://127.0.0.1:5000

## 🔐 Security Note

- Do NOT upload `.env` file to GitHub
- Keep API keys private
- Regenerate keys if exposed

## 🎯 Future Improvements

- Emergency auto-navigation
- ETA calculation
- AI-based hospital recommendation
- Dark mode UI
- Mobile optimization

## 👨‍💻 Author

- Pranjal Patil
