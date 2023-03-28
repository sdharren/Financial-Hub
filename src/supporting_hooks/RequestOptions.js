export const BASE_URL = "http://127.0.0.1:8000/api/";

const createUrl = (base, path) => `${base}${path}`;

export const getData = ({endpoint, endpoint_parameter, authTokens}) => [
    createUrl(BASE_URL, (String(endpoint) + (endpoint_parameter != null ? '?param='+endpoint_parameter : '/'))),
    {
        method: "GET",
        headers:{
            'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access),
        }
    }
];