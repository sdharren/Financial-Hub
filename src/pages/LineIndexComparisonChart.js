import { useState, useEffect, useContext } from "react";
import Chart from "react-apexcharts";
import GraphSelect from "../components/GraphSelect";
import usePlaid from "../custom_hooks/usePlaid";
import useHandleError from "../custom_hooks/useHandleError";

function LineIndexComparisonChart ({ endpoint, endpoint_parameter, selectOptions, updateGraph }) {

    const [comparisonData, error] = usePlaid({endpoint, endpoint_parameter})

    useHandleError(error);

    let handleSelectionUpdate = async(nextParam) => {
        updateGraph({
            'endpoint': endpoint,
            'param': nextParam
        });
    }

    let dates = [];
    let portfolio = [];
    let index = [];
    
    for (let key in comparisonData) {
        dates.push(key);
        portfolio.push({
            x: key,
            y: comparisonData[key]['portfolio']
        });
        
        index.push({
            x: key,
            y:comparisonData[key]['index']
        });
    }

    const series = [  
        {    
            name: 'Portfolio',   
            data: portfolio
        },

        {
            name: 'Index',
            data: index
        }
    ];

    const options = {
    chart: {
        stacked: false,
        height: 100
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [2, 2],
        curve: 'straight'
    },
    xaxis: {
        type: 'datetime',
    },
    yaxis: {
        title: {
        text: 'Value'
        }
    },
    legend: {
        position: 'top',
        horizontalAlign: 'left',
        offsetX: 40
    }
    };

    return (
        <div className='flex flex-col w-full max-h-[30vh]'>
        {
            selectOptions === undefined || selectOptions === null
            ? null
            : <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}/>
        }
        <Chart height = "420vh" options={options} series={series} />
    </div>
    )
}

export default LineIndexComparisonChart;