import ReturnDisplay from "../components/ReturnDisplay";
import PieChart from "./PieChart";

function InvestmentOverview() {
    let {authTokens, logoutUser} = useContext(AuthContext);

    async function getReturns(endpoint, param) {
        let response = await fetch('http://127.0.0.1:8000/api/' + endpoint + (endpoint==='overall_returns'?'/':'/?param='+param),
            {
                method:'GET',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            }
        );
        let data = await response.json();
        return data;
    }

    const returns = getReturns('overall_returns');


    return (
        <div>
            <ReturnDisplay returns={overall_returns}/>
            <PieChart 
                endpoint={endpoint} 
                endpoint_parameter={endpoint_parameter} 
                loadNext={handleLoadNext} 
                updateGraph={handleGraphUpdate}
            />
        </div>
    )
}

export default InvestmentOverview;