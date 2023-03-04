import React, {useContext} from 'react';
import { Link } from "react-router-dom"
import AuthContext from '../context/AuthContext';

export default function Navbar() {
    let {user, logoutUser} = useContext(AuthContext);
    return <nav className="nav"> 
        <Link to = "/" className="site-title">Financial Hub</Link>
        <ul>
            {user && <li><p>Hello, {user.email}</p></li>}
            <li>
                <Link to="/about">About</Link>
            </li>
            <li>
                <Link to="/signup">Sign Up</Link>
            </li>
            <li>
                {user ? (<p onClick = {logoutUser}>Logout</p>): (<Link to ="/login">Login</Link>)}
            </li>
        </ul>
    </nav>
}