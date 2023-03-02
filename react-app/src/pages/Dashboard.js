import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [number, setNumber] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/number/')
      .then(response => {
        setNumber(response.data.number);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <p>The number is {number}</p>
    </div>
  );
}

export default Dashboard;
