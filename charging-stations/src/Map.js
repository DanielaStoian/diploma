import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup } from "react-leaflet";
import axios from "axios";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'react-leaflet-cluster'
import Plot from "react-plotly.js";
import Grid from '@mui/material/Grid';
import { Box, Button, Container, FormControlLabel, FormGroup, Switch } from "@mui/material";

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

const FixGraphData = (props) => {
  let arrOfStr = Array.from(props.data)
  const arrOfNum = arrOfStr.map(str => {
    return parseInt(str, 10);
  });
  let xAxis = Array.from({ length: 168 }, (value, index) => index);
  const trace = {
    x: xAxis,
    y: arrOfNum,
    mode: "lines",
    type: "scatter",
  };
  console.log(trace)
  return(
  <Plot
        data={[trace]}
        layout={{
          title: "Station's Mean",
          height:230,
          width:250,
          margin:{
            l: 20,
            r: 5,  
            b: 30,
            t: 50,
          }
        }}
      />)
}

const Map = () => {
    const position = [37.9, 23.7];
    const [markers, setMarkers] = React.useState();
    const [dhmoi, setDhmoi] = React.useState(true);

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
    <Grid container spacing={2}>
  <Grid item xs={12}>
  {/* <FormGroup>
      <FormControlLabel control={<Switch onChange={()=>{setDhmoi(!dhmoi);console.log(dhmoi)}} />} label="Δήμοι" />
    </FormGroup> */}
  </Grid>
  <Grid item xs={12}>
    <Box padding={0}>
      <MapContainer
      center={position}
      zoom={7}
      style={{ height: "100vh" }}
      maxZoom={15}
      >
      {/* {dhmoi?<MyData />:<div></div>} */}

      <MarkerClusterGroup>
      {markers?markers.map((coord,index) => {return <Marker position={[parseFloat(coord['lat']),parseFloat(coord['long'])]} key={index}>
      <Popup >
        <div>
        <h3>
        Διεύθυνση: {coord['address']} {"               "}
        </h3>
        
        <FixGraphData data={coord['mean']}></FixGraphData>

        <h4>
        Origin: {coord['origin']}
        </h4>
        </div>
      </Popup>

      </Marker> }):null}
      </MarkerClusterGroup>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
    </MapContainer>
    </Box>
  </Grid>
</Grid>
  );
};

export default Map;