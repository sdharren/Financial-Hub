import React, { useContext } from "react";
import { render, screen} from "@testing-library/react";
import userEvent from '@testing-library/user-event'
import Login from "../pages/Login";
import customRender from "./test-utils";

describe("Login component", () => {

    it("renders without crashing", () => {
        customRender(
            <Login />
        )
    })

    it("form has email, password and button field", () => {
        customRender(
            <Login />
        )

        const email_field = screen.getByLabelText(/Email address/i)
        const password_field = screen.getByLabelText(/Password/i)
        const submit_button = screen.getByText('Login')

        expect(email_field).toBeInTheDocument()
        expect(password_field).toBeInTheDocument()
        expect(submit_button).toBeInTheDocument()
    })

    it("email field is of type 'email'", () => {
        customRender(
            <Login />
        )

        const email_field = screen.getByLabelText(/Email address/i)
        expect(email_field).toHaveProperty("type", "email")
    })

    it("password field is of type 'password'", () => {
        customRender(
            <Login />
        )

        const password_field = screen.getByLabelText(/Password/i)
        expect(password_field).toHaveProperty("type", "password")
    })

    it("calls click event", () => {
        const testfn = jest.fn()
        customRender(<Login submit = {testfn}/>)

        const submit_button = screen.getByText('Login')
        userEvent.click(submit_button)

        expect(testfn).toBeCalled()
    }) 
})