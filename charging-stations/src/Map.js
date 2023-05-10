import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup, useMapEvents } from "react-leaflet";
import axios from "axios";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'react-leaflet-cluster'
import Plot from "react-plotly.js";
import Grid from '@mui/material/Grid';
import { Box, Button, Container, FormControlLabel, FormGroup, Paper, styled, Switch } from "@mui/material";

import iconUrl from "./Red_circle.svg";
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

const saveArrival = async (props) => {
  const response = await axios.post(
    "http://127.0.0.1:8000/api/stations/add_arrival/?id=" + props.id + "&start_time=" + props.start_time + "&stay_hours=" + 2, { params:
     { id: props.id, start_time:props.start_time, stay_hours:2} }
  );
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
    textposition: 'auto',
    hoverinfo: 'none',
    marker: {
      color: 'rgb(72,143,237)',
      opacity: 0.6,
      line: {
        color: 'rgb(72,143,237)',
        width: 1.5
    }
  },
  };
  return(


    <Paper variant="elevation0">
      <Box style={{width:'300px',padding:'10px 5px 10px 5px'}} textAlign='center'>

      <h2 style={{fontWeight: '100',display:'inline',textAlign:'center'}}>  Charger types: </h2>
      <h3 style={{fontWeight: '50',display:'inline',textAlign:'center'}}>{props.type}</h3>
      </Box>


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
              bargap: 0.2,
              height:230,
              width:300,
              margin:{
                l: 50,
                r: 20,  
                b: 40,
                t: 50,
              }
            }}
          />
            <Box style={{width:'300px'}} textAlign='center'>
              <Button onClick={() => saveArrival({id:props.id, start_time:12})}>I'm interested</Button>
          </Box>
       </Paper>
      )
}

const Map = (props) => {
    const center = [37.9, 23.7];
    const [zoom, setZoom] = React.useState(7);
    const [markers, setMarkers] = React.useState();
    // const [dhmoi, setDhmoi] = React.useState(true);
    const [position, setPosition] = React.useState();
    const mapRef = React.useRef();
  
    function MyComponent() {
    useMapEvents({
        click(e){
          props.setPosition([e.latlng.lat,e.latlng.lng])
          setPosition(e.latlng)
        },
        zoomend(e){
          setZoom(e.target._animateToZoom)
        }
    })
}
  function getMarkerIcon() {
    const icon = new L.Icon({
      iconSize: [22, 37], // size of the icon
      iconAnchor: [16, 37], 
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    });
    return icon;
  }

  // function getStationIcon() {
  //   const icon = new L.Icon({
  //     iconSize: [32, 50], // size of the icon
  //     iconAnchor: [3, 7], 
  //     iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',

  //   });
  //   return icon;
  // }

  useEffect(() => {
      const getData = async () => {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/stations/get_stations/"
        );
        setMarkers(response.data);
      };
      getData();
    }, []);

    useEffect(() => {
      if (mapRef.current != null){
        mapRef.current.flyTo(props.center, props.zoom);
      }
      }, [props.center]);

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
      center={props.center}
      zoom={props.zoom}
      style={{ height: "100vh" }}
      maxZoom={20}
      ref={mapRef}
      >
      {/* {dhmoi?<MyData />:<div></div>} */}
      { position && <Marker position={position} icon={getMarkerIcon()}>
          </Marker>}
      {/* { <Marker position={props.center} icon={getStationIcon()}>
          </Marker>} */}
      <MarkerClusterGroup>
      {markers?markers.map((coord,index) => {return <Marker position={[parseFloat(coord['lat']),parseFloat(coord['long'])]} key={index}>
      <StyledPop>
        <FixGraphData data={coord['mean']} type={coord['type']} id={coord['id']}></FixGraphData>
      </StyledPop>

      </Marker> }):null}
      </MarkerClusterGroup>
      <MyComponent></MyComponent>
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
