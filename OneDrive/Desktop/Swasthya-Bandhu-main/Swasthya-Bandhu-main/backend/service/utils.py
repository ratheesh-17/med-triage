import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def find_nearest_doctors(user_lat, user_lng, doctors, limit=5):
    for doctor in doctors:
        distance = haversine_distance(user_lat, user_lng, doctor.location_lat, doctor.location_lng)
        doctor.distance_km = round(distance, 2)
    
    sorted_doctors = sorted(doctors, key=lambda d: (d.distance_km, -d.rating))
    return sorted_doctors[:limit]

EMERGENCY_HOSPITALS = [
    {"name": "AIIMS Emergency", "lat": 28.5672, "lng": 77.2100, "phone": "011-26588500"},
    {"name": "Apollo Hospital Emergency", "lat": 28.5494, "lng": 77.2680, "phone": "011-26825858"},
    {"name": "Max Hospital Emergency", "lat": 28.5355, "lng": 77.2490, "phone": "011-26515050"}
]

def find_nearest_emergency_hospital(user_lat, user_lng):
    for hospital in EMERGENCY_HOSPITALS:
        hospital['distance'] = haversine_distance(user_lat, user_lng, hospital['lat'], hospital['lng'])
    
    nearest = min(EMERGENCY_HOSPITALS, key=lambda h: h['distance'])
    return nearest
