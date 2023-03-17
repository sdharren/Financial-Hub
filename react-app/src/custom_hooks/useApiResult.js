import React, { useState, useEffect } from "react";

const useApiResult = ({request, endpoint}) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(request).then(async (response) => {
      if (response.ok) {
        setData(await response.json());
        setError(null);
      } else {
        setError(await response.text());
      }
    })
    .catch((err) => {
      setError(err.message);
    });
  }, [endpoint]);
  return [data, error];
};

export default useApiResult;