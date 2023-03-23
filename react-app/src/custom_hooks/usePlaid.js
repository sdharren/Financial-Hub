import React, { useContext, useMemo } from 'react';
import useApiResult from './useApiResult';
import { getData } from '../requests/RequestOptions';
import AuthContext from '../context/AuthContext';

const usePlaid = ({endpoint, endpoint_parameter, loadNext}) => {
    let {authTokens, logoutUser} = useContext(AuthContext);
    const request = useMemo(() => getData({endpoint, endpoint_parameter, authTokens}), [endpoint, endpoint_parameter]);
    return useApiResult({request, endpoint});
};

export default usePlaid;