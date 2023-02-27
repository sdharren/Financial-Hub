import React from 'react';
import { Link } from "react-router-dom"

export default function Navbar() {
    return <nav className="nav"> 
        <Link to = "/" className="site-title">Financial Hub</Link>
        <ul>
            <li>
                <Link to="/about">About</Link>
            </li>
            <li>
                <Link to="/signup">Sign Up</Link>
            </li>
            <li>
                <Link to="/login">Log In</Link>
            </li>
        </ul>
    </nav>
}