import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import Header from '../components/header';

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
    <>
        <Header
            heading = "Login to your account"
            paragraph= "Don't have an account yet? "
            linkName = "Signup"
            linkUrl = "/signup"
            />
    </>
  )
  
  return form2
}

export default Login
