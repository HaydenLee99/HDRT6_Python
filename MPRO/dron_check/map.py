import folium

# 한국 중심 좌표
CENTER = [36.5, 127.8]

# -----------------------
# 원전 좌표
# -----------------------

nuclear_plants = {
    "Kori": (35.3213,129.2954),
    "Wolsong": (35.7134,129.4758),
    "Hanbit": (35.4105,126.4178),
    "Hanul": (36.9790,129.3840)
}

# -----------------------
# 민간 공항
# -----------------------

airports = {
    "Incheon": (37.4602,126.4407),
    "Gimpo": (37.5583,126.7906),
    "Jeju": (33.5113,126.4928),
    "Gimhae": (35.1795,128.9382),
    "Daegu": (35.8941,128.6589),
    "Cheongju": (36.7166,127.4987),
    "Muan": (34.9914,126.3828),
    "Yangyang": (38.0613,128.6692),
    "Wonju": (37.4412,127.9639),
    "Sacheon": (35.0886,128.0704)
}

# -----------------------
# 군 비행장
# -----------------------

military_airports = {
    "Seongnam Airbase": (37.4442,127.1196),
    "Osan Airbase": (37.0907,127.0293),
    "Suwon Airbase": (37.2395,127.0070)
}

# -----------------------
# 지도 생성
# -----------------------

m = folium.Map(location=CENTER, zoom_start=7)

# -----------------------
# 원전 비행 구역
# -----------------------

for name,(lat,lon) in nuclear_plants.items():

    # 18km 제한구역
    folium.Circle(
        location=[lat,lon],
        radius=18000,
        color="green",
        fill=True,
        fill_opacity=0.25,
        tooltip=f"{name} Nuclear Restricted Zone (18km)"
    ).add_to(m)

    # 3.6km 금지구역
    folium.Circle(
        location=[lat,lon],
        radius=3600,
        color="red",
        fill=True,
        fill_opacity=0.45,
        tooltip=f"{name} Nuclear No-Fly Zone (3.6km)"
    ).add_to(m)


# -----------------------
# 민간 공항 제한구역
# -----------------------

for name,(lat,lon) in airports.items():

    folium.Circle(
        location=[lat,lon],
        radius=9300,
        color="green",
        fill=True,
        fill_opacity=0.25,
        tooltip=f"{name} Airport Restricted Zone"
    ).add_to(m)


# -----------------------
# 군 비행장 제한구역
# -----------------------

for name,(lat,lon) in military_airports.items():

    folium.Circle(
        location=[lat,lon],
        radius=9300,
        color="green",
        fill=True,
        fill_opacity=0.25,
        tooltip=f"{name} Military Airbase Restricted"
    ).add_to(m)


# -----------------------
# 서울 P73 비행금지구역
# -----------------------

seoul_p73_center = [37.5326,126.9900]

folium.Circle(
    location=seoul_p73_center,
    radius=8000,
    color="red",
    fill=True,
    fill_opacity=0.4,
    tooltip="Seoul P73 No Fly Zone"
).add_to(m)


# -----------------------
# 계룡대 군사시설
# -----------------------

folium.Circle(
    location=[36.2762,127.2465],
    radius=3000,
    color="red",
    fill=True,
    fill_opacity=0.4,
    tooltip="Gyeryongdae Military Zone"
).add_to(m)


# -----------------------
# 범례 추가
# -----------------------

legend_html = '''
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 220px;
height: 120px;
background-color: white;
border:2px solid grey;
z-index:9999;
font-size:14px;
padding:10px;
">

<b>Drone Airspace Legend</b><br>
<span style="color:red;">●</span> No Fly Zone<br>
<span style="color:green;">●</span> Restricted Zone<br>
<br>
Red : Flight Prohibited<br>
Green : Flight Restricted

</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))


# -----------------------
# 지도 저장
# -----------------------

m.save("drone_airspace_map.html")

print("지도 생성 완료 → drone_airspace_map.html")