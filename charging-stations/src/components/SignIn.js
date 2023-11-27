import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { useSelector, useDispatch } from 'react-redux'
import { logIn, logOut, setUserId } from '../redux/loginSlice'

const BASE_URL = "http://web:8001"

export default function SignIn() {

  const navigate = useNavigate();
  const [error, setError] = useState(false);
  const isLoggedIn = useSelector((state) => state.login.value)
  const dispatch = useDispatch()

  const getProfile = async (props) => {
    const response = await axios.get(
      BASE_URL +"/api/profiles/get_profile/",{params: {
        email:props.email, password:props.password
      }}
    ).then((response) => {
      setError(false);
      dispatch(logIn())
      dispatch(setUserId(response.data.id))
      navigate('/')
    })
    .catch((response) => {
      if (response.response.status === 404){
        setError(true);
      }
    })
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    getProfile({
      email: data.get("email"),
      password: data.get("password"),
    });
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
          Sign in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            error={error}
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            type = 'email'
            autoFocus
          />
          <TextField
            margin="normal"
            error={error}
            helperText="The email or password is incorrect"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          {/* <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          /> */}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item>
              <Link href="/signup" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}