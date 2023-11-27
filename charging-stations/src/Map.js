import React, { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, GeoJSON, useMap, Marker, Popup, useMapEvents } from "react-leaflet";
import axios from "axios";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'react-leaflet-cluster'
import Plot from "react-plotly.js";
import Grid from '@mui/material/Grid';
import { Box, Button, Checkbox, Container, FormControlLabel, FormGroup, Paper, styled, Switch } from "@mui/material";
import Snackbar from '@mui/material/Snackbar';
import { useSelector, useDispatch } from 'react-redux'
import { logIn, logOut } from './redux/loginSlice'

BASE_URL = "http://web:8001"

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
        BASE_URL + "/api/stations/get_dhm_geojson/"
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
    BASE_URL+"/api/stations/add_arrival/", 
     { id: props.id, start_time:props.start_time, stay_hours:props.stayHours, user_id:props.userId} 
  ).then(response => {
    props.setMessage("Your choice is saved.")
    props.setOpen(true)
  })
  .catch(error => {
   
      props.setMessage("This station is full or not available at the time.")
      props.setOpen(true)
    
  }
  )
};

const getPermission = async (props) => {
  const response = await axios.get(
    BASE_URL+"/api/profiles/get_check_permission/",{ params:
     { id: props.id} }
  ).then(response => {
      saveArrival({id:props.data.id, start_time:props.data.start_time, setOpen:props.data.setOpen, setMessage:props.data.setMessage, stayHours:props.data.stayHours, userId:props.data.userId})
      return true
  })
  .catch(error => {
      props.data.setMessage("You should wait before saving again.")
      props.data.setOpen(true)
      return false
  }
  )
};

const FixGraphData = (props) => {

  const [open, setOpen] = React.useState(false);
  const [message, setMessage] = React.useState("");
  const [checked, setChecked] = React.useState(false);
  const isLoggedIn = useSelector((state) => state.login.value)
  const userId = useSelector((state) => state.login.user_id)
  const dispatch = useDispatch()

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const handleChange = (event) => {
    setChecked(event.target.checked);
  };

  let arrOfStr = Array.from(props.data)
  let arrOfStr2 = Array.from(props.data2)
  const d = new Date();
  let curDay = d.getDay() - 1
  const arrOfNum = arrOfStr.map(str => {
    return parseInt(str, 10);
  });
  const arrOfNum2 = arrOfStr2.map(str => {
    return parseInt(str, 10);
  });
  let arrOfWeek = arrOfNum.slice(24*curDay, 24*(curDay+1))  
  let arrOfWeek2 = arrOfNum2.slice(24*curDay, 24*(curDay+1))  
  let diff = [];
  for(var i = 0; i<=arrOfWeek2.length-1; i++){
    diff.push(arrOfWeek2[i] - arrOfWeek[i]);}

  let xAxis = Array.from({ length: 24 }, (value, index) => index);
  const trace = {
    x: xAxis,
    y: arrOfWeek,
    name: 'Usual traffic',
    type: 'bar',
    textposition: 'auto',
    hoverinfo: 'none',
    marker: {
      color: 'rgb(0,122,242)',
      opacity: 0.6,
      line: {
        color: 'rgb(0,122,242)',
        width: 1.5
    }
  },
  };
  const trace2 = {
    x: xAxis,
    y: diff,
    name: 'Extra traffic',
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


    <Paper variant="elevation0" style={{width:'400px',padding:'10px 5px 10px 5px'}} >
      <Box style={{width:'400px',padding:'10px 5px 10px 5px'}} textAlign='center'>
        <Box style={{width:'400px',padding:'10px 5px 10px 5px'}} textAlign='center'>
          <h2 style={{fontWeight: '150',display:'inline',textAlign:'center', color:'#1976D2'}}> {props.name} </h2>
        </Box>
      <h2 style={{fontWeight: '100',display:'inline',textAlign:'center'}}>  Charger types: </h2>
      <h3 style={{fontWeight: '50',display:'inline',textAlign:'center'}}>{props.type}</h3>
      </Box>


      <Plot
            config = {{
              displayModeBar: false,
            }}
            data={[trace,trace2]}
            layout={{
              title: "Station's Daily Mean",
              xaxis: {
                title: 'Hours',
              },
              yaxis: {
                title: 'Arrivals',
              },
              barmode: 'stack',
              bargap: 0.3,
              height:230,
              width:400,
              margin:{
                l: 50,
                r: 20,  
                b: 40,
                t: 50,
              }
            }}
          />
            <Box style={{width:'400px'}} textAlign='center'>
            <FormControlLabel variant="outlined" size="small"
              control={
                <Checkbox
                  checked={checked} // You are supposed to specify your state here
                  color="primary"
                  name={'checkbox'}
                  onChange={handleChange}
                />
              }
              label={'Interested in visiting?'}
            />
              <Button 
              disabled = {!checked}
              onClick={() => {
                if(isLoggedIn){
                  getPermission({id:userId, data:{id:props.id, start_time:props.time, setOpen:setOpen, setMessage:setMessage, stayHours:props.stayHours, userId:userId} });

                }
                  // if(isLoggedIn){
                  //   saveArrival({id:props.id, start_time:props.time, setOpen:setOpen, setMessage:setMessage, stayHours:props.stayHours, userId:userId})}}
                    else{
                      setOpen(true);setMessage("You must sign in to do that.")}}}
                      >Save my arrival</Button>
              <Snackbar
                anchorOrigin={{vertical: 'top',
                horizontal: 'left'}}
                open={open}
                autoHideDuration={4000}
                onClose={handleClose}
                message={message}
              />
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
          BASE_URL+"/api/stations/get_stations/"
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
        <FixGraphData data={coord['mean']} data2={coord['mean_updating']} type={coord['type']} id={coord['id']} time={props.time} stayHours={props.stayHours} name={coord.name}></FixGraphData>
      </StyledPop>

      </Marker> }):null}
      </MarkerClusterGroup>
      <MyComponent></MyComponent>
      <TileLayer
        attribution="Google Maps"
        url="https://www.google.cn/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}"
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
