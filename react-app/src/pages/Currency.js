import PieChart from "./PieChart";
import { useState } from "react";

function Currency() {
    const [graph, setGraph] = useState(<PieChart endpoint={"currency_data"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'currency_data': 'currency_data',
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <PieChart endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }


    return (
        <div className="">
            {graph}
        </div>
    );
}

export default Currency;
