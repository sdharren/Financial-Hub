import {Route, Redirect, Navigate} from 'react-router-dom';

// const PrivateRoute = ({user, children}) => {
//     console.log("private route works");
//     return (
//         <Route {...rest}>{children}</Route>
//     );
// };

const PrivateRoute = ({children}) => {

    const authenticated = false;
    if (!authenticated) {
        return <Navigate to="/login" replace />
    }

    return children;
};

export default PrivateRoute;