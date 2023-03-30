/**
 * Creates the login component for logging in users. Uses AuthContext(loginUser)
 * to authenticate users.
 */
import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import Header from '../components/header';
import { loginFields } from '../components/formFields';
import Input from '../components/input';
import FormAction from '../components/formAction';
import { backgroundBox } from '../static/styling';
import '../static/errors.css';

const fields = loginFields;
let fieldState = {};
fields.forEach(field => fieldState[field.id] = '');

const Login = ({submit}) => {

  let {loginUser, error} = useContext(AuthContext);

  let form2 = (
    <div className={"login-container mt-20 mb-20 mx-20 p-10 " + backgroundBox}>
        <Header
            heading = "Login to your account"
            paragraph= "Don't have an account yet? "
            linkName = "Signup"
            linkUrl = "/signup"
        />
        <form className = "mt-8 space-y-6" onSubmit = {submit === undefined ? loginUser : submit}>
            <div className = "-space-y-px">
                {
                    fields.map(field=>
                        <div key = {field.key}>
                            <Input
                                key={field.id}
                                handleChange={null}
                                labelText={field.labelText}
                                labelFor={field.labelFor}
                                id={field.id}
                                name={field.name}
                                type={field.type}
                                isRequired={field.isRequired}
                                placeholder={field.placeholder}
                            />
                            <p className = {"error " + field.name + "-error"}>{error}</p>
                        </div>
                    )  
                }
            </div>
            <FormAction data-testid='login-form'handleSubmit={loginUser} text = "Login" />
        </form>
       </div>
  )
  
  return form2
}

export default Login
