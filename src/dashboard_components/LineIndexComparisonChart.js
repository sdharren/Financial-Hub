import Chart from "react-apexcharts";
import GraphSelect from "../components/GraphSelect";
import usePlaid from "../custom_hooks/usePlaid";
import useHandleError from "../custom_hooks/useHandleError";
import { lineGraphSizing } from "../static/styling";

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
            y: comparisonData[key]['portfolio'].toFixed(2)
        });
        
        index.push({
            x: key,
            y:comparisonData[key]['index'].toFixed(2)
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
        labels: {
            style: {
                colors: '#fff'
            }   
        }
    },
    yaxis: {
        show: true,
            showAlways: true,
            tickAmount: 6,
            labels: {
                formatter: function (value) {
                    return '$' + value;
                },
                show: true,
                align: 'right',
                minWidth: 0,
                maxWidth: 160,
                style: {
                    colors: ['#fff'],
                    fontSize: '12px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 400,
                    cssClass: 'apexcharts-yaxis-label',
                },
                offsetX: 0,
                offsetY: 0,
                rotate: 0,
            },
            axisBorder: {
                show: true,
                color: '#fff',
                offsetX: 0,
                offsetY: 0
            },
        title: {
        text: 'Value',
        style: {
            color: '#fff',
        },
        }
    },
    legend: {
        position: 'top',
        horizontalAlign: 'left',
        offsetX: 40,
        labels: {
            colors: '#fff'
        }
    }
    };

    return (
        <div className={lineGraphSizing}>
        {
            selectOptions === undefined || selectOptions === null
            ? null
            : <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}/>
        }
        <Chart height = "420vh" options={options} series={series ? series : {}} />
    </div>
    )
}

export default LineIndexComparisonChart;