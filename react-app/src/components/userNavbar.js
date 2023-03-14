import React from 'react';
import { Link } from "react-router-dom"

export default function UserNavbar() {
    let {user, logoutUser} = useContext(AuthContext);
    return <nav className="nav"> 
        <Link to = "/" className="site-title">Financial Hub</Link>
        <ul>
            
                {user && <li><p>Hello, {user.email}</p></li>}
            
            <li>
                <Link to="/dashboard">Dashboard</Link>
            </li>
            <li>
                <Link to="/link_assets">Link Assets</Link>
            </li>
            <li>
                <Link to="/accounts">Accounts</Link>
            </li>
            <li>
                {user ? (<p onClick = {logoutUser}>Logout</p>): (<Link to ="/login">Login</Link>)}
            </li>
        </ul>
    </nav>
}