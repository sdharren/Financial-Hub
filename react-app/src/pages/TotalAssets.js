import { useState } from "react";
import PieChart from "./PieChart";

function TotalAssetsDisplay({handleClicked}) {
    const [graph, setGraph] = useState(<PieChart endpoint={"total_assets"} loadNext={handleClicked}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'total_assets': 'total_assets'
    }

    return (
        <div style={{width: '45rem', margin: 'auto', padding: '2rem'}}>
            {graph}
        </div>
    );
}

export default TotalAssetsDisplay;