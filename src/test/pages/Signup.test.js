import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Signup from "../../pages/Signup";
import { customRenderNoUser } from "../test-utils";
import userEvent from "@testing-library/user-event";

describe("Signup component", () => {
    let mockLoginUser;
    let mockSignupUser;

  beforeEach(() => {
    mockLoginUser = jest.fn();
    mockSignupUser = jest.fn();
  });
    it("renders without crashing", () => {
        customRenderNoUser(
            <Signup />
        )
    })

    it("has first and last name, email, password and password confirmation fields", () => {
        customRenderNoUser(
            <Signup />
        )

        const firstName = screen.getByLabelText(/First Name/i)
        const lastName = screen.getByLabelText(/Last Name/i)
        const password = screen.getByLabelText('Password')
        const email = screen.getByLabelText(/Email address/i)
        const passconf = screen.getByLabelText(/Confirm password/i)

        expect(firstName).toBeInTheDocument()
        expect(lastName).toBeInTheDocument()
        expect(email).toBeInTheDocument()
        expect(password).toBeInTheDocument()
        expect(passconf).toBeInTheDocument()
    })

    it("email field is of type 'email'", () => {
        customRenderNoUser(
            <Signup />
        )

        const email_field = screen.getByLabelText(/Email address/i)
        expect(email_field).toHaveProperty("type", "email")
    })

    it("password field is of type 'password'", () => {
        customRenderNoUser(
            <Signup />
        )

        const password_field = screen.getByLabelText('Password')
        expect(password_field).toHaveProperty("type", "password")
    })

    it("password confirmation field is of type 'password'", () => {
        customRenderNoUser(
            <Signup />
        )

        const password_conf_field = screen.getByLabelText(/Confirm Password/i)
        expect(password_conf_field).toHaveProperty("type", "password")
    })

    it("has a register button", () => {
        customRenderNoUser(
            <Signup />
        )

        const registerButton = screen.getByText('Register')
        expect(registerButton).toBeInTheDocument()
    })

    it("register is of type 'submit'", () => {
        customRenderNoUser(
            <Signup />
        )

        const registerButton = screen.getByText('Register')
        expect(registerButton).toHaveProperty('type', 'submit')
    })

    it("register button calls function on click", () => {
        const testfn = jest.fn(e => e.preventDefault())
        customRenderNoUser(
            <Signup submit={testfn}/>
        )

        const registerButton = screen.getByText('Register')
        userEvent.click(registerButton)
        expect(testfn).toBeCalled()
    })

})