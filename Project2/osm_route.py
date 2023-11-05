import overpy
import folium
from api import get_elevation

def get_trails_near_location(lat, lon, radius=40000, limit=300):
    api = overpy.Overpass()

    query_str = f"""
    way
      (around:{radius},{lat},{lon})
      ["highway"="path"];
    (._;>;);
    out body;
    """
    
    result = api.query(query_str)
    trails = []
    cnt = 0
    for way in result.ways:
        trail_coords = [(node.lat, node.lon) for node in way.nodes]
        trails.append({"coordinates": trail_coords})
        cnt = cnt + 1
        if(cnt == limit):
            break
    return trails


lat, lon = 48.721106440877264, -113.77452742759156
coo_start = lat, lon  
trails = get_trails_near_location(lat, lon)
#for i, trail in enumerate(trails):      
    #print(f"Trail {i + 1}:")
    #print(f"  Coordinates: {trail['coordinates']}")   
#     j = j + 1
#     coordinates_float = [(float(lat), float(lon)) for lat, lon in trail['coordinates']]
#     print(coordinates_float[j])
#     m = folium.Map(location=list(coordinates_float[j]), zoom_start=32)
#     path = folium.PolyLine(locations=coordinates_float, color="blue", weight=4, opacity=1).add_to(m)
    
# first_trail_coords = list(map(float, trails["Trail 1"][0]))



mapbox_access_token = 'pk.eyJ1IjoicGl0b3RjaGVuIiwiYSI6ImNsb2t2OXA3cjE5a2oya3FvMXRzcmtoM2IifQ.q9xG_pLcQcmd7gP734u72A'
mapbox_tiles = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{{z}}/{{x}}/{{y}}?access_token={mapbox_access_token}"
m = folium.Map(location=coo_start, zoom_start=13, tiles=mapbox_tiles, attr='Mapbox')

#m = folium.Map(location=coo_start, zoom_start=13)
buf =0
sum0 = 0.00
for trail in trails:
    float_coordinates = [(float(lat), float(lon)) for lat, lon in trail['coordinates']]
    float_coordinates = []
    for lat, lon in trail['coordinates']:
        lat_float = float(lat)
        lon_float = float(lon)
        float_coordinates.append((lat_float, lon_float))
        elv = get_elevation(lat_float,lon_float)       
        diff = abs(elv - buf)
        buf = elv
        print(f"diff:{diff} ")
        sum0 = sum0 + diff
        print(elv)
    print(f"sum:{sum0}")
    marker = folium.Marker(
        location=[lat_float,lon_float],
        popup=folium.Popup(str(sum0), parse_html=True),
        tooltip='point to view elevation')
    marker.add_to(m)
          
    folium.PolyLine(locations=float_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)    
  
    
    #print(f"  Length: {trail['length']} km")
m.save('map.html')
