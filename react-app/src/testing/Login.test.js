import React from "react";
import { render } from "@testing-library/react";
import Login from "../pages/Login";
import { AuthProvider } from "../context/AuthContext";
import { BrowserRouter } from "react-router-dom";

describe("Login component", () => {
    it("renders without crashing", () => {
        render(
            <BrowserRouter>
                <AuthProvider>
                    <Login />
                </AuthProvider>
            </BrowserRouter>
        )
    })
})