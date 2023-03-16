import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import { signupFields } from '../components/formFields';
import Input from '../components/input'
import FormAction from '../components/formAction';
import Header from '../components/header';

// need to add confirmation that passwords match

const Signup = () => {

    const fields = signupFields;
    let fieldState = {};
    fields.forEach(field => fieldState[field.id] = '');

    let {loginUser} = useContext(AuthContext);

    let signupUser = async (e) => {
        e.preventDefault();
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
                if (data.hasOwnProperty(key)) {
                    alert(data[key])
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