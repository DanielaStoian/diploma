import React, { useEffect, useState } from "react";
import { AppBar, Button, IconButton, Paper, Toolbar, Typography, Card, TextField, Grid, Box, Container, Tabs, Tab } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Autocomplete from "react-google-autocomplete";
import { usePlacesWidget } from "react-google-autocomplete";
import MapLocation from "./components/MapLocation";
import styled from 'styled-components';
import "./ChooseLocation.css"
import Map from "./Map";
const API_KEY = "AIzaSyCaKPzbKvamce5K7H6-kkP6wRrunpxamLw";

const AutoComplete = () => {
  const { ref } = usePlacesWidget({
    apiKey:API_KEY,
    onPlaceSelected: (place) => {
      console.log(place.geometry.location.lat());
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
            <Tabs centered value={tabIndex} onChange={handleTabChange} variant={'fullWidth'}>
              <Tab label="Choose Location" />
              <Tab label="Choose Station" />
              <Tab label="Done" />
            </Tabs>
            {tabIndex === 0 && (
          <Grid container spacing={2} alignContent={'center'}>
          <Grid item xs={6} align="center">
          <Container style={{padding : 50}} sx={{height: "100%", display: "flex", width:"100%"}}>
            <Paper sx={{height: "100%" ,width:"100%"}}>
              <Title>
                Type your destination
              </Title>
              <div>
              <AutoComplete/>

              </div>
              <div style={{padding:"300px 0px 0px 0px"}}>
              <Button size="large" variant="contained" onClick={() => setTabIndex(1)}>
                Next
              </Button>
              </div>
              </Paper>
            </Container>
              </Grid>
              <Grid item xs={6} align="center">
                <Container style={{padding : 50}} sx={{height: "100%", display: "flex", width:"100%"}}>
              <Paper sx={{height: "100%" ,width:"100%"}}>
              <Title>
                ...or pick it directly on the map
              </Title>
              <MapLocation></MapLocation>
              </Paper>
                </Container>
            </Grid>

          </Grid>
            )}
            {tabIndex === 1 && (
              <Grid container spacing={2} alignContent={'center'}>
                <Grid item xs={12} align="center">
                  <Paper sx={{height: "50%" ,width:"70%"}}>
                    <Map></Map>
                  </Paper>
                </Grid>
              </Grid>
        )}
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
  width: 50%;
  outline: none;
  font-size: 25px;
  &:focus {
      background-size: 100% 2px, 100% 1px;
      outline: 0 none;
      transition-duration: 0.3s;
      color: #525252;
    }
`;

const Title = styled.h1`
font-weight: 200;
padding: 50px 0px 70px 0px;
color: #13213c
`