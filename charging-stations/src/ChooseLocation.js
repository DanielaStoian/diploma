import React, { useEffect, useState } from "react";
import { AppBar, Button, IconButton, Paper, Toolbar, Typography, Card, TextField, Grid, Box, Container, Tabs, Tab, Checkbox, Input } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Autocomplete from "react-google-autocomplete";
import { usePlacesWidget } from "react-google-autocomplete";
import MapLocation from "./components/MapLocation";
import styled from 'styled-components';
import "./ChooseLocation.css"
import Map from "./Map";
import { MobileTimePicker } from '@mui/x-date-pickers/MobileTimePicker';
import axios from "axios";
import ResponsiveTimePickers from "./TimePicker";
import TypeSelect from "./TypePicker";
const API_KEY = "AIzaSyCaKPzbKvamce5K7H6-kkP6wRrunpxamLw";

const AutoComplete = (props) => {
  const { ref } = usePlacesWidget({
    apiKey:API_KEY,
    onPlaceSelected: (place) => {
      // console.log(place.geometry.location);
      props.setPosition([place.geometry.location.lat(),place.geometry.location.lng()])
    },
    options: {
      strictBounds: false,
      types: ["address"],
      componentRestrictions: { country: "gr" },
      language:["gr"]
    },
  });
  return <_Input ref={ref}></_Input>
}

const ChooseLocation = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [radius, setRadius] = useState(1);
  const [winner, setWinner] = useState();
  const [center, setCenter] = useState([37.9, 23.7]);
  const [zoom, setZoom] = useState(7);
  const [position, setPosition] = useState();
  const [type, setType] = useState('');

  const fetchStation = async () => {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/stations/get_radius/", { params:
       { radius: radius, lat : position[0], long:position[1], start_time:6, stay_hours:2, type:type } }
    );
    console.log(response.data)
    setWinner([response.data.lat,response.data.long]);
    setCenter([response.data.lat,response.data.long]);

    setZoom(15);
  };

  const handleTabChange = (event, newTabIndex) => {
    setTabIndex(newTabIndex);
  };
      return (
        <div>
            <AppBar position="static">
              <Toolbar>
                <IconButton
                  size="large"
                  edge="start"
                  color="inherit"
                  aria-label="menu"
                  sx={{ mr: 2 }}
                >
                  <MenuIcon />
                </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Choose Your Destination
            </Typography>
            <Button color="inherit">Login</Button>
          </Toolbar>
            </AppBar>
          <Grid container spacing={0} alignContent={'center'}>
          <Grid item xs={2} >
          <Container style={{padding : "50px 0px 0px 35px"}} sx={{height: "100%",  width:"100%"}}>
              <Title>
                Type your destination
              </Title>
              <div>
              <AutoComplete setPosition={setPosition}/>
              </div>
              <Title>
                Radius (km)
              </Title>
              <Input
                value={radius}
                size="small"
                onChange={(event) => {
                  setRadius(event.target.value === '' ? '' : Number(event.target.value));
                }}
                onBlur={() => {
                  if (radius < 0) {
                    setRadius(0);
                  } else if (radius > 20) {
                    setRadius(20);
                  }}}
                inputProps={{
                  step: 1,
                  min: 0,
                  max: 20,
                  type: 'number',
                  'aria-labelledby': 'input-slider',
                }}
              />
              {/* <Title>
                What time will you arrive?
              </Title>
               <ResponsiveTimePickers/> */}
               <Title>
                Select your charger type
              </Title>
               <TypeSelect setType={setType}></TypeSelect>
              <div style={{padding:"200px 0px 0px 0px"}}>
              <Button size="large" variant="contained" onClick={() => fetchStation()}>
                Show best Station
              </Button>
              </div>
            </Container>
              </Grid>
              <Grid item xs={10} align="center">
                <Container style={{padding : 10}} sx={{height: "100%", display: "flex", width:"100%"}}>

              <Map center={center} zoom={zoom} position={position} setPosition={setPosition}></Map>

                </Container>
            </Grid>

          </Grid>

        </div>
      );
  };

  export default ChooseLocation;

  const _Input = styled.input`
  background-image: linear-gradient(#20aee3, #20aee3), linear-gradient(#bfbfbf, #bfbfbf);
  border: 0 none;
  border-radius: 0;
  box-shadow: none;
  float: none;
  background-color: transparent;
  background-position: center bottom, center calc(100% - 1px);
  background-repeat: no-repeat;
  background-size: 0 2px, 100% 1px;
  padding: 0;
  transition: background 0s ease-out 0s;
  color: #bfbfbf;
  min-height: 35px;
  display: initial;
  width: 70%;
  outline: 1;
  font-size: 25px;
  &:focus {
      background-size: 100% 2px, 100% 1px;
      outline: 0 none;
      transition-duration: 0.3s;
      color: #525252;
    }
`;

const Title = styled.h3`
font-weight: 200;
// padding: 50px 0px 70px 0px;
color: #13213c
`