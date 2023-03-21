import {createContext, useState, useEffect} from 'react';
import jwt_decode from 'jwt-decode';
import {useNavigate} from 'react-router-dom';

const AuthContext = createContext();

// you cannot type links because everytime you type a link, the app "refreshes"
// and calls updateToken(), which then calls logoutUser() and redirects to
// "login/"

export const AuthProvider = ({ children }) => {

    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
    let [loading, setLoading] = useState(true)

    const navigate = useNavigate()

    async function cache_assets(method) {
        await fetch('http://127.0.0.1:8000/api/cache_assets/', {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
        });
    }

    let loginUser = async (e )=> {
        e.preventDefault();
        let response = await fetch('http://127.0.0.1:8000/api/token/', {
            method : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'email':e.target.email_address.value, 'password':e.target.password.value})
        })
        let data = await response.json()
        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))

            cache_assets('PUT');
            
            navigate('/dashboard')
        }
        else {
            alert("Something went wrong!")
        }
    };

    let logoutUser = () => {
        cache_assets('DELETE');

        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        navigate("/login")
    }

    let updateToken = async () => {
        console.log("update token called")
        let response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
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