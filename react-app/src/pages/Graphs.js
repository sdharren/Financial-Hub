import React, { useState, useEffect } from 'react';
import axios from 'axios';
import{ Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'react-chartjs-2';
ChartJS.register(BarElement,CategoryScale,
LinearScale,
Tooltip,
Legend);

function Graphs() {
  const options = {}
  const data = {
    labels : ['Mon','Tue','Wed','Thur','Fri'],
    datasets : [{
      label : 'numbs',
      data : [3,4,5,5,6],
      borderColor : 'black',
      backgroundColor: ['aqua','red'],
      borderWidth: 1,
    }]
  }


  return (
    <div>
      <Bar
      data = {data}
      options = {options}></Bar>
    </div>
  );
}

export default Graphs;
