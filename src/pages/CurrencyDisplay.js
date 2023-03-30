import PieChart from "../dashboard_components/PieChart";
import { useState } from "react";

function CurrencyDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"currency_data"} loadNext={handleLoadNext} currency={'%'} />);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'currency_data': 'currency_data',
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <PieChart endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext} currency={'%'} />
        );
    }


    return (
        <div className="">
            {graph}
        </div>
    );
}

export default CurrencyDisplay;
