/**
 * The AuthContext component that handles the authentication of the user. The
 * authentication uses the react-Context object so that auth information can be
 * passed to all child components.
 */
import {createContext, useState, useEffect} from 'react';
import jwt_decode from 'jwt-decode';
import {useNavigate} from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
    let [loading, setLoading] = useState(true)
    let [error, setError] = useState('')

    const navigate = useNavigate()

    async function cache_assets(method, tokens) {
        console.log("cache with " + method);
        await fetch('api/cache_assets/', {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':'Bearer ' + String(tokens.access)
                }
        });
    }

    let loginUser = async (e )=> {
        e.preventDefault();
        let response = await fetch('api/token/', {
            method : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'email':e.target.email_address.value, 'password':e.target.password.value})
        })
        let data = await response.json()
        
        // store user in local cache if credentials are authenticated
        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))

            await cache_assets('PUT', data)
            .then(navigate('/dashboard'));
        }
        // show alert if credentials do not match
        else {
            alert(data["detail"])
            setError(data["detail"])
        }
    };

    let logoutUser = () => {
        cache_assets('DELETE', authTokens);

        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        navigate("/login")
    }

    // update function that will get called by useEffect to refresh the 
    // authentication token
    let updateToken = async () => {
        let response = await fetch('api/token/refresh/', {
            method : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'refresh':authTokens?.refresh})
        })

        let data = await response.json()

        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
        }
        else {
            logoutUser()
        }

        if (loading) {
            setLoading(false)
        }
    }

    let contextData = {
        user:user,
        authTokens:authTokens,
        loginUser:loginUser,
        logoutUser:logoutUser
    };

    useEffect(() => {

        if (loading) {
            updateToken()
        }

        let fourMinutes = 1000 * 60 * 4
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, fourMinutes)
        return () => clearInterval(interval)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
}

export default AuthContext;
