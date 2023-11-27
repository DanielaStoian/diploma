import { Paper, TextField } from "@mui/material";
import { useRef, useEffect } from "react";
import L from "leaflet";
import React from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup, useMapEvents } from "react-leaflet";


const MapLocation = () => {
  const [position, setPosition] = React.useState();
  function MyComponent() {
    useMapEvents({
        click(e){
          setPosition(e.latlng)
        }
    })
}
  function getMarkerIcon() {
    const icon = new L.Icon({
      iconSize: [22, 37], // size of the icon
      iconAnchor: [16, 37], 
      iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
    });
    return icon;
  }
    return (
     <Paper style={{width:1000, height:800}}>
        <MapContainer center={[37.9, 23.7]} zoom={7} style={{width:"100%", height:"100%"}}>
          <MyComponent></MyComponent>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
          { position && <Marker position={position} icon={getMarkerIcon()}>
            
          </Marker>}
          
        </MapContainer>
     </Paper>

    );
   };

export default MapLocation;