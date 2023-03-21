import React from "react";
import { render } from "@testing-library/react";
import Signup from "../pages/Signup";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";

describe("Signup component", () => {
    it("renders without crashing", () => {
        render(
            <BrowserRouter>
                <AuthProvider>
                    <Signup />
                </AuthProvider>
            </BrowserRouter>
        )
    })
})