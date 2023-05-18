import React from "react";
import ChooseLocation from "./ChooseLocation";
// import "./styles.css";
import Map from "./Map";

import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";

export default function App() {
  return (
    <div>
     <Routes>
        <Route path="/" element={ <ChooseLocation/> } />
        <Route path="signin" element={ <SignIn/> } />
        <Route path="signup" element={ <SignUp/> } />
      </Routes>
    </div>
);
}
