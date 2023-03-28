import PieChart from "../dahsboard_components/PieChart";
import BarGraph from "../dahsboard_components/BarGraph";
import { useState } from "react";
import DropDown from "./DropDown";

function BalancesDisplay() {
    const [graph, setGraph] = useState(<PieChart endpoint={"get_balances_data"} loadNext={handleLoadNext}/>);

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'get_balances_data': 'select_account',
        'select_account': 'get_balances_data',
    }

    // passed as a parameter to the pie chart to update this page once a section of the pie chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <PieChart endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext}/>
        );
    }

    function handleOnChange(event) {
        setGraph(
            <BarGraph endpoint={'yearly_graphs'} endpoint_parameter={'yearly_graphs'} loadNext={handleLoadNext}/>
        );
    }

    return (
        <div className="balance-graph">
            {graph}
            <DropDown className='' onChange={handleOnChange}/>
        </div>
    );
}

export default BalancesDisplay;
