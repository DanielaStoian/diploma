import { Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Paper } from "@mui/material";
import { useState } from "react"
import styled from 'styled-components';
  function ShowDrawer(props) {

    const getList = () => (
      <div style={{ width: 280 }} onClick={() => props.setOpen(false)}>
        {/* <Button onClick={() => props.setOpen(false)} style={{float: 'right'}}>Back</Button> */}
        {props.data.length==0 ?<Title>No matching results found</Title> :props.data.map((item,index) => (
          <ListItem button key={index} onClick={() => props.setCenter([item[1][0].lat,item[1][0].long])}>
            <List>
              {console.log(item)}
                <Header>{item[1][0].name}</Header>
                <div>
                  <Wrtiting>
                    {item[1][1]}% matching
                    <div style={{ width: 10, height:10 }}></div> 
                    {item[1][0].price}€ / kWh
                    <div >
                    {item[0].toFixed(2)} km away
                    </div>
                  </Wrtiting>
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
  const Wrtiting = styled.h4`
  font-weight: 50;
//   padding: 50px 50px 50px 50px;
  color: #13213c
  `
  export default ShowDrawer;