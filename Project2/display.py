import folium
import requests
import webbrowser

def get_elevation(latitude, longitude, api_key):
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"
    params = {
        "locations": f"{latitude},{longitude}",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            elevation = data["results"][0]["elevation"]
            return elevation
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    api_key = "AIzaSyD9BRgtHmmIYyqRmy92puu3U6KVd9W3BqI"
    latitude = 27.988333
    longitude = 86.925278
    elevation = get_elevation(latitude, longitude, api_key)

    if elevation is not None:
        print(f"海拔高度（米）：{elevation}")

        # 创建地图对象
        m = folium.Map(location=[latitude, longitude], zoom_start=15)
        
        # 在地图上添加标记
        folium.Marker(
            location=[latitude, longitude],
            popup=f"海拔高度（米）：{elevation}"
        ).add_to(m)

        # 保存地图为HTML文件
        map_filename = "elevation_map.html"
        m.save(map_filename)
        print(f"地图已保存为 {map_filename} 文件。")

        # 使用默认浏览器打开地图文件
        webbrowser.open(map_filename, new=2)
    else:
        print("无法获取海拔高度信息。")
