import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [number, setNumber] = useState(null);

  useEffect(() => {
    axios.get('/api/number/')
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

