import PieChart from "./PieChart";
import { useState, useEffect } from "react";
import axios from 'axios';

function GraphDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"investment_categories"} loadNext={handleLoadNext}/>);
    const [json_data, setJsonData] = useState();

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/stocks_json/')
          .then(response => {
            setJsonData(response.data)
          })
          .catch(error => {
            console.log(error);
          });
      }, []);

    console.log(json_data);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'investment_categories': 'investment_category_breakdown',
        'investment_category_breakdown': 'stock_history'
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <PieChart endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }


    return (
        <div style={{width: '45rem', margin: 'auto', padding: '2rem'}}>
            {graph}
        </div>
    );
}

export default GraphDisplay;