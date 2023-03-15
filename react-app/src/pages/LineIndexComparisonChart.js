import { useState, useEffect, useContext } from "react";
import Chart from "react-apexcharts";
import { useNavigate } from "react-router-dom";
import AuthContext from '../context/AuthContext';

function LineIndexComparisonChart () {
    const [portfolio, setPortfolio] = useState(null);
    const [index, setIndex] = useState(null);

    const navigate = useNavigate();

    let {authTokens, logoutUser} = useContext(AuthContext);

    
        // 

    useEffect (() => {
        const get_data = async() =>  {
            let url = 'http://127.0.0.1:8000/api/portfolio_comparison/?param=^FTSE';
            let response = await fetch(url, {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            });
            console.log("request sent");
            let data = await response.json();
            if (response.status === 200) {
                console.log("received 200")
                console.log(data);
            }
            else if (response.status === 303) {
                if (data['error'] === 'Investments not linked.') {
                    navigate('/plaid_link');
                }
            }
        }
        get_data();
        console.log("here");
    }, []);


    const series = [  
        {    
            name: 'Portfolio',   
            data: [30, 40, 35, 50, 49, 60, 70, 91, 125, 130]
        },

        {
            name: 'Index',
            data: [20, 22, 30, 45, 60, 90, 105, 120, 135, 150]
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
        categories:  [1,2,3,4,5,6,7,8,9,0], // THIS IS WHERE THE DATES GO
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