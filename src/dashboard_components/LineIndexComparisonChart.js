import { useState, useEffect, useContext } from "react";
import Chart from "react-apexcharts";
import { useNavigate } from "react-router-dom";
import AuthContext from '../context/AuthContext';

function LineIndexComparisonChart () {
    const [comparisonData, setComparisonData] = useState(null);

    const navigate = useNavigate();

    let {authTokens, logoutUser} = useContext(AuthContext);

    
        // 

    useEffect (() => {
        const get_data = async() =>  {
            let url = 'api/portfolio_comparison/?param=^FTSE';
            let response = await fetch(url, {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            });

            let data = await response.json();
            
            if (response.status === 200) {
                setComparisonData(data);
            }
            else if (response.status === 303) {
                if (data['error'] === 'Investments not linked.') {
                    navigate('/plaid_link');
                }
            }
        }
        get_data();
    }, []);

    let dates = [];
    let portfolio = [];
    let index = [];
    
    for (let key in comparisonData) {
        dates.push(key);
        portfolio.push(comparisonData[key]['portfolio']);
        index.push(comparisonData[key]['index']);
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
        // type: 'line',
        stacked: true,
        height: 350
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [2, 2],
        curve: 'smooth'
    },
    xaxis: {
        //type: 'datetime', COMMENTED THIS OUT FOR TESTING
        categories:  dates, // THIS IS WHERE THE DATES GO
    },
    yaxis: {
        title: {
        text: 'Value'
        }
    },
    fill: {
        opacity: [0.8, 0.8],
        gradient: {
        inverseColors: false,
        shade: 'light',
        type: 'vertical',
        opacityFrom: 0.85,
        opacityTo: 0.55,
        stops: [0, 100]
        }
    },
    legend: {
        position: 'top',
        horizontalAlign: 'left',
        offsetX: 40
    }
    };

    // const chart = new ApexCharts(document.querySelector('#chart'), options);


    // chart.render();
    return (
        <div>
            <Chart options={options} series={series} />
        </div>
    )
}

export default LineIndexComparisonChart;