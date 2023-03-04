import React, {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'

const HomePage = () => {

    let {authTokens} = useContext(AuthContext)
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
        setFirstName(data["first_name"])
    }

    return (
        <div>
            <p>You are logged in {firstName}!</p>
        </div>
    )
}

export default HomePage
