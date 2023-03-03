import PieChart from "./Graphs";
import { useState } from "react";

function BarChartDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"monthly_graphs"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'monthly_graphs': 'weekly_graphs',
        'weekly_graphs': ''
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

export default BarChartDisplay;
