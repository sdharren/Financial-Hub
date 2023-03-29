import {Outlet, Navigate} from 'react-router-dom';
import { useContext } from 'react'
import AuthContext from '../context/AuthContext';

const OnlyPublicRoutes = ({children}) => {

    let {user} = useContext(AuthContext)
    return (
        !user ? <Outlet/> : <Navigate to='/dashboard' />
    );
};

export default OnlyPublicRoutes;