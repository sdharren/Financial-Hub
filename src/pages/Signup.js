/**
 * Creates the Signup component. Provides the user with a form to enter details
 * to register user. Performs checks on email and passwords before sending api
 * request to server.
 */
import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import { signupFields } from '../components/formFields';
import Input from '../components/input'
import FormAction from '../components/formAction';
import Header from '../components/header';
import { backgroundBox } from '../static/styling';
import '../static/errors.css';

const Signup = ({submit}) => {

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
        let response = await fetch('api/signup/', {
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
        else {
            alert(Object.values(data).join("\n"))
        }
    }
     
    let form2 = (
        <div className={"signup-container my-10 mx-20 p-10 " + backgroundBox}>
            <Header 
                heading = "Register your account"
                paragraph = "Already have an account? "
                linkName= "Login here"
                linkUrl='/login'
            />
            <form className = "mt-8 space-y-6" onSubmit={submit === undefined ? signupUser : submit}>
                <div className='-space-y-px'>
                    {
                        fields.map(field =>
                            <div key = {field.key}>
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
                                <p className = {"error " + field.name + "-error"}></p>

                            </div>
                        )
                    }
                    <FormAction handleSubmit={signupUser} text = "Register" />
                </div>
            </form>
        </div>
    )

    return form2
}

export default Signup