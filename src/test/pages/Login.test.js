import React, { useContext } from "react";
import { render, screen, act, fireEvent} from "@testing-library/react";
import userEvent from '@testing-library/user-event'
import Login from "../../pages/Login";
import {customRenderNoUser} from "../test-utils";

describe("Login component", () => {

    it("renders without crashing", () => {
        customRenderNoUser(
            <Login />
        )
    })

    it("form has email, password and button field", () => {
        customRenderNoUser(
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
        customRenderNoUser(
            <Login />
        )

        const email_field = screen.getByLabelText(/Email address/i)
        expect(email_field).toHaveProperty("type", "email")
    })

    it("password field is of type 'password'", () => {
        customRenderNoUser(
            <Login />
        )

        const password_field = screen.getByLabelText(/Password/i)
        expect(password_field).toHaveProperty("type", "password")
    })

    it("calls click event", () => {
        const testfn = jest.fn(e => e.preventDefault())
        customRenderNoUser(<Login submit = {testfn}/>)

        const submit_button = screen.getByText('Login')
        userEvent.click(submit_button)

        expect(testfn).toBeCalled()
    }) 

    it('should update the email state when the user types in the email input', () => {
        customRenderNoUser(<Login />);
        const email_field = screen.getByLabelText(/Email address/i)
    
        act(() => {
          fireEvent.change(email_field, { target: { value: 'test@test.com' } });
        });
    
        expect(email_field.value).toBe('test@test.com');
      });
    
      it('should update the password state when the user types in the password input', () => {
        customRenderNoUser(<Login />);
        const password_field = screen.getByLabelText(/Password/i)
    
        act(() => {
          fireEvent.change(password_field, { target: { value: 'testpassword' } });
        });
    
        expect(password_field.value).toBe('testpassword');
      });
})