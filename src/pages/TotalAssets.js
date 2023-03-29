import { useState } from "react";
import PieChart from "../dashboard_components/PieChart";

function TotalAssetsDisplay({handleClicked}) {
    const [graph, setGraph] = useState(<PieChart endpoint={"total_assets"} loadNext={handleClicked}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'total_assets': 'total_assets'
    }

    return (
        <div>
            {graph}
        </div>
    );
}

export default TotalAssetsDisplay;
