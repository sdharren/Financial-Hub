import {Outlet, Navigate} from 'react-router-dom';

// const PrivateRoute = ({user, children}) => {
//     console.log("private route works");
//     return (
//         <Route {...rest}>{children}</Route>
//     );
// };

const PrivateRoutes = ({children}) => {

    const authenticated = false;
    // if (!authenticated) {
    //     return <Navigate to="/login" />
    // }

    // return children;
    return (
        authenticated ? <Outlet/> : <Navigate to='/login' />
    );
};

export default PrivateRoutes;