import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import Header from '../components/header';
import { loginFields } from '../components/formFields';
import Input from '../components/input';

const fields = loginFields;
let fieldState = {};
fields.forEach(field => fieldState[field.id] = '');

const Login = () => {

  let {loginUser} = useContext(AuthContext);


  let form1 = (
    <div>
        <form onSubmit={loginUser}>
            <input type = "text" name = "email" placeholder='Enter email:' />
            <input type = "password" name='password' placeholder='Enter password'/>
            <input type = "submit"/>
        </form>
    </div>
  )

  let form2 = (
    <div>
        <Header
            heading = "Login to your account"
            paragraph= "Don't have an account yet? "
            linkName = "Signup"
            linkUrl = "/signup"
        />
        <form className = "mt-8 space-y-6">
            <div className = "-space-y-px">
                {
                    fields.map(field=>
                        <Input
                            key={field.id}
                            handleChange={loginUser}
                            labelText={field.labelText}
                            labelFor={field.labelFor}
                            id={field.id}
                            name={field.name}
                            type={field.type}
                            isRequired={field.isRequired}
                            placeholder={field.placeholder}
                        />
                
                    )  
                }
            </div>
        </form>
       </div>
  )
  
  return form2
}

export default Login
