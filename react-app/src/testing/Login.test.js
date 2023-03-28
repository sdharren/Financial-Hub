import React, { useContext } from "react";
import { render, screen, getByLabelText} from "@testing-library/react";
import Login from "../pages/Login";
import AuthContext, { AuthProvider } from "../context/AuthContext";
import { BrowserRouter, Router} from "react-router-dom";
import Home from "../pages/Home";
import customRender from "./test-utils";

describe("Login component", () => {

    it("renders without crashing", () => {
        customRender (
            <Login />
        )
    })

    it("has email and password field", async () => {
        
        customRender(
            <Login />
        )
        screen.debug()
        const email_field = screen.getByLabelText(/Email address/i)
        const password_field = screen.getByLabelText(/Password/i)
        const submit_button = screen.getByText('Login')

        expect(email_field).toBeInTheDocument()
        expect(password_field).toBeInTheDocument()
        expect(submit_button).toBeInTheDocument()
    })
})