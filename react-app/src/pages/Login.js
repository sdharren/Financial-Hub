import React from 'react'

const Login = () => {
  return (
    <div>
        <form>
            <input type = "text" name = "email" placeholder='Enter email:' />
            <input type = "password" name='password' placeholder='Enter password'/>
            <input type = "submit"/>
        </form>
    </div>
  )
}

export default Login
