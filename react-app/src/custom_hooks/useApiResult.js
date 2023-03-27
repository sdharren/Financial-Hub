import React, { useState, useEffect } from "react";

const useApiResult = ({request, endpoint}) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [url, headers] = request

  useEffect(() => {
    fetch(url, headers).then(async (response) => {
        if (response.ok) {
            setData(await response.json());
            setError(null);
        } 
      else if (response.status === 303) {
        setError(await response.json());
      }
      else {
        setError(response.statusText);
      }
    })
    .catch((err) => {
      setError(err.message);
    });
  }, [request, endpoint]);
  return [data, error];
};

export default useApiResult;