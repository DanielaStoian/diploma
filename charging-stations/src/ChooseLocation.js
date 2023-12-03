import React, { useEffect, useState } from "react";
import { AppBar, Button, IconButton, Paper, Toolbar, Typography, Card, TextField, Grid, Box, Container, Tabs, Tab, Checkbox, Input } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { usePlacesWidget } from "react-google-autocomplete";
import styled from 'styled-components';
import "./ChooseLocation.css"
import Map from "./Map";
import axios from "axios";
import dayjs from 'dayjs';
import ResponsiveTimePickers from "./TimePicker";
import TypeSelect from "./TypePicker";
import ShowDrawer from "./components/Drawer";
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux'
import { logIn, logOut } from './redux/loginSlice'

const API_KEY = "AIzaSyA7QTg9sKaaDyzNny0k9sr-7r8jEN5DLZI";
BASE_URL=process.env.REACT_APP_BASE_URL

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
  const [radius, setRadius] = useState(1);
  const [winner, setWinner] = useState([]);
  const [center, setCenter] = useState([37.9, 23.7]);
  const [zoom, setZoom] = useState(7);
  const [position, setPosition] = useState();
  const [type, setType] = useState('');
  const [open, setOpen] = useState(false);
  const [time, setTime] = useState(dayjs('2022-04-17T15:30'));
  const [stayHours, setStayHours] = useState(2);
  const navigate = useNavigate();
  const isLoggedIn = useSelector((state) => state.login.value)
  const dispatch = useDispatch()

  function distance(lat1, lon1, lat2, lon2) {
    // approximate radius of earth in km
    const R = 6373.0;
    lat1 = toRadians(lat1);
    lon1 = toRadians(lon1);
    lat2 = toRadians(lat2);
    lon2 = toRadians(lon2);

    const dlon = lon2 - lon1;
    const dlat = lat2 - lat1;

    const a = Math.sin(dlat / 2)**2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const distance = R * c;

    return distance;
}

function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

  const fetchStation = async () => {
    const response = await axios.get(
      BASE_URL+ +"api/stations/get_radius/", { params:
       { radius: radius, lat : position[0], long:position[1], start_time:time.$H, stay_hours:stayHours, type:type } }
    ).then((response => {
      var arr = []
      // setWinner(response.data);
      for(let i=0; i < response.data.length; i++){
        let lat = response.data[i][0]['lat']
        let long = response.data[i][0]['long']
        let dist = distance(lat,long,position[0],position[1])
        arr.push([dist,response.data[i]])
      }
      setWinner(arr)
    }))
    .catch(error => {
      setWinner([])
    })
    // this needs to be moved to the drawer
    // setCenter([response.data.lat,response.data.long]);

    setZoom(18);
  };

      return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
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
            <Button color="inherit" onClick={() => {dispatch(logOut());navigate('/signin')}}>{isLoggedIn?'Logout':'Login'}</Button>
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
               <Title>
                Select your charger type
              </Title>
               <TypeSelect setType={setType}></TypeSelect>

              <Title>
                What time will you arrive?
              </Title>

              <DemoContainer components={['TimePicker']}>
                <TimePicker label="Time picker" value={time} defaultValue={dayjs('2022-04-17T15:30')} disablePast={true}
                  onChange={(newValue) => setTime(newValue)} slotProps={{
                    textField: { error: false,},
                  }}/>
              </DemoContainer>

              <Title>
                How many hours will you stay?
              </Title>
              <Input
                value={stayHours}
                size="small"
                onChange={(event) => {
                  setStayHours(event.target.value === '' ? '' : Number(event.target.value));
                }}
                onBlur={() => {
                  if (radius < 0) {
                    setStayHours(0);
                  } else if (radius > 24) {
                    setStayHours(24);
                  }}}
                inputProps={{
                  step: 1,
                  min: 0,
                  max: 24,
                  type: 'number',
                  'aria-labelledby': 'input-slider',
                }}
              />
              <div style={{padding:"150px 0px 0px 0px"}}>
              <Button size="large" variant="contained" onClick={() => {fetchStation();setOpen(true)}}>
                show recommended stations
              </Button>
              <ShowDrawer data={winner} setCenter={setCenter} open={open} setOpen={setOpen}></ShowDrawer>
              </div>
            </Container>
              </Grid>

              <Grid item xs={10} align="center">
                <Container style={{padding : 10}} sx={{height: "100%", display: "flex", width:"100%"}}>
              <Map center={center} zoom={zoom} position={position} setPosition={setPosition} time={time.$H} stayHours={stayHours}></Map>

                </Container>
            </Grid>

          </Grid>

        </div>
      </LocalizationProvider>
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
  width: 100%;
  outline: 1;
  font-size: 15px;
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