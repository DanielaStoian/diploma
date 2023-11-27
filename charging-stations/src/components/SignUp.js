import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux'
BASE_URL = "web:8001"

export default function SignUp() {

  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const addProfile = async (props) => {
    const response = await axios.post(
      BASE_URL +"/api/profiles/add_profile/",{
        first_name:props.first_name, last_name:props.last_name, email:props.email, password:props.password
      }
    ).then((response) => {
      setError(false);
      navigate('/signin');
    })
    .catch((response) => {
      if (response.response.status === 302){
        setError(true)
      }
    })
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    addProfile({first_name:data.get("firstName"), last_name:data.get("lastName"), email:data.get("email"), password:data.get("password")} )

  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          boxShadow: 3,
          borderRadius: 2,
          px: 4,
          py: 6,
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
        <TextField
            margin="normal"
            required
            fullWidth
            name="firstName"
            label="First Name"
            id="first_name"
          />    
          <TextField
            margin="normal"
            required
            fullWidth
            name="lastName"
            label="Last Name"
            id="last_name"
          />          
          <TextField
            margin="normal"
            error={error}
            helperText="This email is already used"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            type='email'
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item>
              <Link href="/signin" variant="body2">
                {"Already have an account? Sign In"}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}