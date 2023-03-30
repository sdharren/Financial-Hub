/**
 * Contains the form fields for the login page and the sign up page.
 */
const loginFields = [
    {
        key : 1,
        labelText : "Email address",
        labelFor : "email_address",
        id : "email_address",
        name : "email_address",
        type : "email",
        autocomplete : "email_address",
        isRequired : true,
        placeholder : "Email address"
    },
    {
        key : 2,
        labelText : "Password",
        labelFor : "password",
        id : "password",
        name : "password",
        type : "password",
        autocomplete : "current_password",
        isRequired : true,
        placeholder : "Password"
    }
]

const signupFields = [
    {
        key : 1,
        labelText : "First Name",
        labelFor : "first_name",
        id : "first_name",
        name : "first_name",
        type : "text",
        autocomplete : "first_name",
        isRequired : true,
        placeholder : "First Name"
    },
    {
        key : 2,
        labelText : "Last Name",
        labelFor : "last_name",
        id : "last_name",
        name : "last_name",
        type : "text",
        autocomplete : "last_name",
        isRequired : true,
        placeholder : "Last Name"
    },
    {
        key : 3,
        labelText : "Email address",
        labelFor : "email_address",
        id : "email_address",
        name : "email_address",
        type : "email",
        autocomplete : "email_address",
        isRequired : true,
        placeholder : "Email address" 
    },
    {
        key : 4,
        labelText : "Password",
        labelFor : "password",
        id : "password",
        name : "password",
        type : "password",
        autocomplete : "current_password",
        isRequired : true,
        placeholder : "Password"
    },
    {
        key : 5,
        labelText : "Confirm password",
        labelFor : "confirm_password",
        id : "confirm_password",
        name : "confirm_password",
        type : "password",
        autocomplete : "confirm_password",
        isRequired : true,
        placeholder : "Confirm password"
    },
]

export {loginFields, signupFields};