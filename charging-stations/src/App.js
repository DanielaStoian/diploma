import React from "react";
import ChooseLocation from "./ChooseLocation";
// import "./styles.css";
import Map from "./Map";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

export default function App() {
  return (
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <ChooseLocation />
</LocalizationProvider>);
}
