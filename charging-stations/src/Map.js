import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup } from "react-leaflet";
import axios from "axios";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'react-leaflet-cluster'

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;


const MyData = () => {
  const [data, setData] = React.useState();
  const map = useMap();

  useEffect(() => {
    const getData = async () => {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/stations/get_dhm_geojson/"
      );
      setData(response.data);
    };
    getData();
  }, []);

  if (data) {
    // These next 3 lines purely for debuggins:
    const geojsonObject = L.geoJSON(data);
    map.fitBounds(geojsonObject.getBounds());
    console.log(geojsonObject);
    // end debugging

    return <GeoJSON data={data}/>;
  } else {
    return null;
  }
};

const Map = () => {
    const position = [37.9, 23.7];
    const [markers, setMarkers] = React.useState();

    useEffect(() => {
        const getData = async () => {
          const response = await axios.get(
            "http://127.0.0.1:8000/api/stations/get_stations/"
          );
          setMarkers(response.data);
        };
        getData();
      }, []);

  return (
      <MapContainer
      center={position}
      zoom={7}
      style={{ height: "100vh" }}
      maxZoom={14}
      >
      <MyData />

      <MarkerClusterGroup>
      {markers?markers.map((coord,index) => {return <Marker position={[parseFloat(coord['lat']),parseFloat(coord['long'])]} key={index}>
      <Popup>
        <div>
        {coord['address']}
        </div>
        <div>
        {coord['origin']}
        </div>
      </Popup>

      </Marker> }):null}
      </MarkerClusterGroup>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
    </MapContainer>
  );
};

export default Map;