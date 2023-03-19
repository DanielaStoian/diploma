// import React, {useState} from "react";
// import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
// import './App.css';
// // import { Icon } from "leaflet";
// // import * as parkData from "./data/skateboard-parks.json";

// function MapApp() {
//   return (
//     <MapContainer center={[37.9, 23.7]} zoom={7}scrollWheelZoom={true}>
//       <TileLayer
//     url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//     attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
//       />
//     </MapContainer>
//   );
// }

// export default MapApp

import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import zipUrl from "./tm.zip";
import Shapefile from "./Shapefile";

export default function Leaflet() {

  
  const position = [37.9, 23.7];
  return (
    <MapContainer
      center={position}
      zoom={7}
      style={{ height: "100vh" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      <Shapefile zipUrl={zipUrl} />
    </MapContainer>
  );
}
