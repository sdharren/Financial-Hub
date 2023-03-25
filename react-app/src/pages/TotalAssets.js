import { useState } from "react";
import PieChart from "./PieChart";

function TotalAssetsDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"total_assets"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'total_assets': 'total_assets'
    }

    function handleLoadNext(event) {
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

export default TotalAssetsDisplay;
