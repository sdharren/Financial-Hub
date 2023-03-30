/**
 * Creates the <Navbar /> component. Contains the main application logo that
 * redirects to the home page (dashboard if logged in).
 * Contains about, signup and login if user is not logged in.
 * Contains link assets, manage assets and my-account if user is logged in.
 */
import React, {useContext, useEffect, useState} from 'react';
import { Link } from "react-router-dom"
import AuthContext from '../context/AuthContext';
import '../static/navbar.css';
import logo from '../images/logo3.png';

export default function Navbar() {
    let {user, logoutUser, authTokens} = useContext(AuthContext);
    let [firstName, setFirstName] = useState("")

    useEffect( () => {
        getFirstName()
    })

    // returns the first name of the user logged in.
    let getFirstName = async() => {
        let response = await fetch('/api/firstname/', {
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

    // default form when user is not logged in
    let defaultForm = (
        <ul className='flex w-full justify-end gap-10 items-center'>
            <li>
                <Link to="/about">About</Link>
            </li>
            <li>
                <Link to="/signup">Sign up</Link>
            </li>
            <li>
                <Link to ="/login">Log in</Link>
            </li>
        </ul>
    );

    // form when user is logged in
    let loggedInForm = (
        <ul className='flex w-full justify-end gap-10 items-center'>
            <li>
                {user && <p className='text-green-500'>Hello, {firstName}!</p>}
            </li>
            <li>
                <Link to = "/link_assets">Link assets</Link>
            </li>
            <li>
                <Link to = "/accounts">Manage linked assets</Link>
            </li>
            <li>
                <div className='nb_dropdown'>
                    <button className='nb_dropbtn'>My account</button>
                    <div className='nb_dropcontent'>
                        {/* <div>
                            <a href='#'>Settings</a>
                        </div>
                        <hr className='hrbreak'></hr> */}
                        <p className="nav-logout" onClick = {logoutUser}>Logout</p>
                    </div>
                </div>
            </li>
        </ul>
    );

    return (
        <nav className="nav border-white border-b-2" data-testid="navbar">
            <div className='navbarContents text-white flex pt-5 pb-3 px-2'>
                <Link to = {user ? "/dashboard" : "/"} className="site-title text-4xl font-bold">
                    <img className='aspect-auto max-h-[6vh]' src={logo} alt='logo'/>
                </Link>
                {user ? loggedInForm : defaultForm}
            </div>
        </nav>
    )
}