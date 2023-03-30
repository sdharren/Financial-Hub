import { useState } from "react";
import BarGraph from "../dashboard_components/BarGraph";
import DropDown from "./DropDown";

function BarChartDisplay() {
    const [graph, setGraph] = useState(
        <div>
            <BarGraph endpoint={"sector_spending"} endpoint_parameter={'fda'} loadNext={handleLoadNext}/>
            <DropDown endpoint={"sector_sending"} endpoint_parameter={'fda'} loadNext={handleOnChange}/>
        </div>
    );

    // JSON to know which API endpoint to query next
    const nextRoute = {
        'sector_spending': 'company_spending',
        'company_spending': 'company_spending',
    }

    // passed as a parameter to the bar chart to update this page once a section of the bar chart is clicked
    function handleLoadNext(event) {
        console.log(nextRoute[event.current]);
        setGraph(
                <div>
                    <BarGraph endpoint={nextRoute[event.current]} endpoint_parameter={event.next} loadNext={handleLoadNext}/>
                </div>
        );
    }

    function handleLoadPrevious(event){
        setGraph(
            <div>
                <BarGraph endpoint='sector_spending' endpoint_parameter={event.next} loadNext={handleLoadNext}/>
                <DropDown endpoint={"sector_spending"} endpoint_parameter={'fda'} loadNext={handleOnChange}/>
            </div>
        );
    }

    function handleOnChange(event) {
        setGraph(
            <div>
                <BarGraph endpoint={"sector_spending"} endpoint_parameter={event['name']} loadNext={handleLoadNext}/>
                <DropDown className='' endpoint={event['endpoint']} endpoint_parameter={event['param']} loadNext={handleOnChange}/>
            </div>
        );
    }


    return (
        <div className='w-full text-white'>
            <button onClick={handleLoadPrevious}>
                Go Back
            </button>
            {graph}
        </div>
    );
}

export default BarChartDisplay;
