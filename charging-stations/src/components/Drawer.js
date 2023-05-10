import { Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Paper } from "@mui/material";
import { useState } from "react"
import styled from 'styled-components';
  function ShowDrawer(props) {

    const getList = () => (
      <div style={{ width: 280 }} onClick={() => props.setOpen(false)}>
        {props.data.length==0 ?<Title>No matching results found</Title> :props.data.map((item, index) => (
          <ListItem button key={index} onClick={() => props.setCenter([item.lat,item.long])}>
            <List>
                <Header>{item.name}</Header>
                <div>
                    {item.address}
                </div>
            </List>
            {/* <ListItemText primary={item.name} /> */}
          </ListItem>
        ))}
        <Button onClick={() => props.setOpen(false)} style={{float: 'right'}}>Back</Button>
      </div>
    );
    return (
      <div>
        <Drawer open={props.open} anchor={"left"} onClose={() => props.setOpen(false)} variant={"persistent"}> 
          {getList()}
        </Drawer>
      </div>
    );
  }
  
  const Title = styled.h3`
  font-weight: 200;
  padding: 50px 50px 50px 50px;
  color: #13213c
  `
  const Header = styled.h3`
  font-weight: 100;
//   padding: 50px 50px 50px 50px;
  color: #13213c
  `

  export default ShowDrawer;