import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function TypeSelect(props) {
  const [type, setType] = React.useState('');

  const handleChange = (event) => {
    setType(event.target.value);
    props.setType(event.target.value);
  };

  return (
    <Box sx={{ minWidth: 100, maxWidth: 200 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Type</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={type}
          label="Type"
          onChange={handleChange}
        >
          <MenuItem value={1}>AC Type 2</MenuItem>
          <MenuItem value={2}>CCS Type 2</MenuItem>
          <MenuItem value={3}>Mode 3</MenuItem>
          <MenuItem value={4}>CHAdeMO</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}