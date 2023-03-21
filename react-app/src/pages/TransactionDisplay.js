import { useState } from "react";
import BarGraph from "./BarGraph";
import DropDown from "./DropDown";

function BarChartDisplay() {
    const [graph, setGraph] = useState(<BarGraph endpoint={"yearly_graphs"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'yearly_graphs': 'monthly_graphs',
        'monthly_graphs': 'weekly_graphs',
        'weekly_graphs': 'weekly_graphs'
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
            <BarGraph endpoint='yearly_graphs' endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }


    return (
        <div style={{width: '45rem', margin: 'auto', padding: '2rem'}}>
            <button onClick={handleLoadPrevious}>
                Go Back
            </button>
            {graph}
            <DropDown/>
        </div>
    );
}

export default BarChartDisplay;
