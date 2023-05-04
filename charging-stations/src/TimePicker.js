import 'react-time-picker/dist/TimePicker.css';
import 'react-clock/dist/Clock.css';
import React, { useState } from 'react';
import TimePicker from 'react-time-picker';
export default function ResponsiveTimePickers() {
      const [value, onChange] = useState('10:00');
    
      return (
        <div style={{padding:"10px 0px 0px 0px"}}>
          <TimePicker onChange={onChange} value={value} disableClock={true}/>
        </div>
      );
    }