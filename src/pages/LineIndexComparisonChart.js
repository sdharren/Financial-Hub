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
            let url = 'api/portfolio_comparison/?param=^GDAXI';
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
        portfolio.push({
            x: key,
            y: comparisonData[key]['portfolio']
        });
        
        index.push({
            x: key,
            y:comparisonData[key]['index']
        });
    }

    console.log(portfolio)
    console.log(index)
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
        height: 350
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
        <div>
            <Chart options={options} series={series} />
        </div>
    )
}

export default LineIndexComparisonChart;