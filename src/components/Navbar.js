import React, {useContext, useEffect, useState} from 'react';
import { Link } from "react-router-dom"
import AuthContext from '../context/AuthContext';
import '../static/navbar.css';

export default function Navbar() {
    let {user, logoutUser, authTokens} = useContext(AuthContext);
    let [firstName, setFirstName] = useState("")

    useEffect( () => {
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
            setFirstName(data["first_name"].charAt(0).toUpperCase() + 
                         data["first_name"].slice(1))
        }
        else if (response.statusText === 'Unauthorized') {
            logoutUser()
        }
    }

    let defaultForm = (
        <ul className='flex w-full justify-end gap-10 items-center'>
            <li>
                <Link to="/about">About</Link>
            </li>
            <li>
                <Link to="/signup">Sign Up</Link>
            </li>
            <li>
                <Link to ="/login">Login</Link>
            </li>
        </ul>
    );

    // let loggedInForm = (
    //     <ul>
    //         <li>
    //             {user && <p>Hello, {firstName}</p>}
    //         </li>
    //         <li>
    //             <Link to = "/balances">Bank accounts</Link>
    //         </li>
    //         <li>
    //             <Link to = "/currency">Currencies</Link>
    //         </li>
    //         <li>
    //             <Link to = "/list">Transactions</Link>
    //         </li>
    //         <li>
    //             <Link to = "/bar_graph_display">Bar graph</Link>
    //         </li>
    //         <li>
    //             <p className="nav-logout" onClick = {logoutUser}>Logout</p>
    //         </li>
    //     </ul>
    // );

    let loggedInForm = (
        <ul className='flex w-full justify-end gap-10 items-center'>
            <li>
                {user && <p className='text-green-500'>Hello, {firstName}!</p>}
            </li>
            <li>
                <Link to = "/link_assets">Link assets</Link>
            </li>
            <li>
                <Link to = "/accounts">Managed linked assets</Link>
            </li>
            <li>
                <div className='nb_dropdown'>
                    <button className='nb_dropbtn'>My account</button>
                    <div className='nb_dropcontent'>
                        <div>
                            <a href='#'>Settings</a>
                        </div>
                        <hr className='hrbreak'></hr>
                        <p className="nav-logout" onClick = {logoutUser}>Logout</p>
                    </div>
                </div>
            </li>
        </ul>
    );

    return (
        <nav className="nav border-white border-b-2" data-testid="navbar">
            <div className='navbarContents text-white flex pt-5 pb-3 px-2'>
                <Link to = {user ? "/dashboard" : "/"} className="site-title text-4xl font-bold">DASH.</Link>
                {user ? loggedInForm : defaultForm}
            </div>
        </nav>
    )
    // decide on size for the main application window
}
