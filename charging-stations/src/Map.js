import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup } from "react-leaflet";
import axios from "axios";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'react-leaflet-cluster'
import Plot from "react-plotly.js";
import Grid from '@mui/material/Grid';
import { Box, Button, Container, FormControlLabel, FormGroup, Paper, styled, Switch } from "@mui/material";

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
    // console.log(geojsonObject);
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
  let arrOfWeek = arrOfNum.slice(0, 24)  
  let xAxis = Array.from({ length: 24 }, (value, index) => index);
  const trace = {
    x: xAxis,
    y: arrOfWeek,
    type: 'bar',
    text: arrOfWeek.map(String),
    textposition: 'auto',
    hoverinfo: 'none',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
    }
  }
  };
  return(
    // <Paper variant="elevation0">
      <Plot
            data={[trace]}
            layout={{
              title: "Station's Daily Mean",
              xaxis: {
                title: 'Hours',
              },
              yaxis: {
                title: 'Arrivals',
              },
              barmode: 'stack',
              height:230,
              width:250,
              margin:{
                l: 50,
                r: 20,  
                b: 40,
                t: 50,
              }
            }}
          />
      // </Paper>
      )
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
      <StyledPop>
        {/* <h3>
        Διεύθυνση: {coord['address']} {"               "}
        </h3> */}
        
        <FixGraphData data={coord['mean']}></FixGraphData>

        {/* <h4>
        Origin: {coord['origin']}
        </h4> */}
      </StyledPop>

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

const StyledPop = styled(Popup)`
  border-radius: 0;
  .leaflet-popup-content-wrapper {
    border-radius: 0;
    background-color: transparent;
    box-shadow: none;
  }

  .leaflet-popup-tip-container {
    visibility: hidden;
  }
`;