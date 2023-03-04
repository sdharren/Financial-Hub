import {Outlet, Navigate} from 'react-router-dom';
import { useContext } from 'react'
import AuthContext from '../context/AuthContext';

// const PrivateRoute = ({user, children}) => {
//     console.log("private route works");
//     return (
//         <Route {...rest}>{children}</Route>
//     );
// };

const PrivateRoutes = ({children}) => {

    let {user} = useContext(AuthContext)
    // if (!authenticated) {
    //     return <Navigate to="/login" />
    // }

    // return children;
    return (
        user ? <Outlet/> : <Navigate to='/login' />
    );
};

export default PrivateRoutes;