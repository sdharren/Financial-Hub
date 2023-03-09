import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';

const Signup = () => {

let {loginUser} = useContext(AuthContext);

    let SignupUser = async (e) => {
        e.preventDefault();
        let response = await fetch('http://127.0.0.1:8000/api/signup/', {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({
                'email' : e.target.email.value,
                'first_name' : e.target.first_name.value,
                'last_name' : e.target.last_name.value,
                'password' : e.target.password.value
            })
        })

        let data = await response.json()
        // response 400: email : "user with this email already exists."
        // response 400: password: 
        if (response.status === 200) {
            loginUser(e)
        }

        // response 200:

    }
    
    return (
        <div>
            <form onSubmit={SignupUser}>
            <input type = "text" name = "email" placeholder='Enter email:' />
            <input type = "text" name = "first_name" placeholder='Enter first name:' />
            <input type = "text" name = "last_name" placeholder='Enter last name:' />
            <input type = "password" name='password' placeholder='Enter password'/>
            <input type = "submit"/>
            </form>
        </div>
    )
}

export default Signup