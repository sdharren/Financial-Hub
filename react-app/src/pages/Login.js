import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import Header from '../components/header';
import { loginFields } from '../components/formFields';
import Input from '../components/input';
import FormAction from '../components/formAction';
import FormExtra from '../components/formExtra';
import '../static/css/errors.css';

// add remember me functionality

const fields = loginFields;
let fieldState = {};
fields.forEach(field => fieldState[field.id] = '');

const Login = () => {

  let {loginUser} = useContext(AuthContext);

  let form2 = (
    <div>
        <Header
            heading = "Login to your account"
            paragraph= "Don't have an account yet? "
            linkName = "Signup"
            linkUrl = "/signup"
        />
        <form className = "mt-8 space-y-6" onSubmit = {loginUser}>
            <div className = "-space-y-px">
                {
                    fields.map(field=>
                        <div>
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
                            <p class = {"error " + field.name + "-error"}></p>
                        </div>
                    )  
                }
            </div>
            <FormAction handleSubmit={loginUser} text = "Login" />
        </form>
       </div>
  )
  
  return form2
}

export default Login
