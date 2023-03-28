import React, {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'

const HomePage = () => {

    let {authTokens, logoutUser} = useContext(AuthContext)
    let [firstName, setFirstName] = useState([])
    useEffect(() => {
        getFirstName()
    })

    let getFirstName = async() => {
        let response = await fetch('http://127.0.0.1:8000/api/firstname/', {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        })
        let data = await response.json()

        if (response.status === 200) {
            setFirstName(data["first_name"])
        }
        else if (response.statusText === 'Unauthorized') {
            logoutUser()
        }
    }

    return (
        <div data-testid= 'homepagetest'>
            <p>You are logged in {firstName}!</p>
        </div>
    )
}

export default HomePage
