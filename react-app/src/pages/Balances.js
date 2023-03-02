import PieChart from "./PieChart";
import { useState } from "react";

function BalancesDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"get_balance_data"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'get_balances_data': 'balances',
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

export default BalancesDisplay;
