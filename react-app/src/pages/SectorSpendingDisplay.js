import { useState } from "react";
import BarGraph from "../dashboard_components/BarGraph";

function BarChartDisplay() {
    const [graph, setGraph] = useState(<BarGraph endpoint={"sector_spending"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'sector_spending': 'company_spending',
        'company_spending': 'company_spending',
    }

    // passed as a parameter to the bar chart to update this page once a section of the bar chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <BarGraph endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }

    function handleLoadPrevious(event){
        setGraph(
            <BarGraph endpoint='sector_spending' endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }


    return (
        <div style={{width: '45rem', margin: 'auto', padding: '2rem'}}>
            <button onClick={handleLoadPrevious}>
                Go Back
            </button>
            {graph}
        </div>
    );
}

export default BarChartDisplay;
