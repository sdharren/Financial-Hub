import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import { signupFields } from '../components/formFields';
import Input from '../components/input'
import FormAction from '../components/formAction';
import Header from '../components/header';
import '../static/errors.css';

// need to add confirmation that passwords match

const Signup = () => {

    const fields = signupFields;
    let fieldState = {};
    fields.forEach(field => fieldState[field.id] = '');

    let {loginUser} = useContext(AuthContext);

    let checkPassword = (e) => {
        if (e.target.password.value !== e.target.confirm_password.value) {
            document.querySelector(".password-error").innerHTML = "Passwords do not match"
            document.querySelector(".password-error").style.display = "block"
            return false
        }
        return true
    }

    let signupUser = async (e) => {
        e.preventDefault();
        if (!checkPassword(e)) {
            return
        }
        let response = await fetch('http://127.0.0.1:8000/api/signup/', {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({
                'email' : e.target.email_address.value,
                'first_name' : e.target.first_name.value,
                'last_name' : e.target.last_name.value,
                'password' : e.target.password.value
            })
        })

        let data = await response.json()
        
        if (response.status === 200) {
            loginUser(e)
        }
        else if (response.status === 400) {
            for (var key in data) {
                if (key === "email") {
                    document.querySelector(".email-error").innerHTML = data[key];
                    document.querySelector(".email_error").style.display = "block";
                }
                if (key === "password") {
                    document.querySelector(".password-error").innerHTML = data[key];
                    document.querySelector(".password_error").style.display = "block";
                }
            }
        }
    }
    
    let form1 = (
        <div class="super-signup-container">
        <div class="signup-container">
            <form onSubmit={signupUser}>
            <input type = "text" name = "email" placeholder='Enter email:' />
            <input type = "text" name = "first_name" placeholder='Enter first name:' />
            <input type = "text" name = "last_name" placeholder='Enter last name:' />
            <input type = "password" name='password' placeholder='Enter password'/>
            <input type = "submit"/>
            </form>
        </div>
        </div>
    )
    
    let form2 = (
        <div class="super-signup-container">
        <div class="signup-container">
        <div>
            <Header 
                heading = "Register your account"
                paragraph = "Already have an account? "
                linkName= "Login here"
                linkUrl='/login'
            />
            <form className = "mt-8 space-y-6" onSubmit={signupUser}>
                <div className=''>
                    {
                        fields.map(field =>
                            <div>
                                <Input 
                                    key = {field.id}
                                    handleChange = {null}
                                    labelText = {field.labelText}
                                    labelFor = {field.labelFor}
                                    id = {field.id}
                                    name = {field.name}
                                    type = {field.type}
                                    isRequired = {field.isRequired}
                                    placeholder = {field.placeholder}
                                />
                                <p class = {"error " + field.name + "-error"}>hello</p>

                            </div>
                        )
                    }
                    <FormAction handleSubmit={signupUser} text = "Register" />
                </div>
            </form>
        </div>
        </div>
        </div>
    )

    return form2
}

export default Signup