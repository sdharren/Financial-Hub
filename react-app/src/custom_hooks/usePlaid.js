import React, { useContext, useMemo } from 'react';
import AuthContext from '../context/AuthContext';
import useApiResult from './useApiResult';
import { getData } from '../requests/RequestOptions';

const usePlaid = ({endpoint, endpoint_parameter, loadNext}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const request = useMemo(() => getData({endpoint, endpoint_parameter, authTokens}), []);
    return useApiResult({request, endpoint});
};

export default usePlaid;