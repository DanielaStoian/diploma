import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import axios from "axios";

const MyData = () => {
  const [data, setData] = React.useState();
  const map = useMap();

  useEffect(() => {
    const getData = async () => {
      const response = await axios.get(
        "https://gist.githubusercontent.com/UmairMughal901/d43ee77a9be27f2dcd006038fe8f07e7/raw/8650f4f3585ff0c1706da7a434251cfc70f1907b/map.geojson"
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

    return <GeoJSON data={data} />;
  } else {
    return null;
  }
};
const position = [37.9, 23.7];
const Map = (props) => {
  return (
      <MapContainer
      center={position}
      zoom={7}
      style={{ height: "100vh" }}
      >
      <MyData />
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
    </MapContainer>
  );
};

export default Map;