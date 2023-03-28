import React, { createContext } from "react";
import { render } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const user = {
    "token_type": "access",
    "exp": 2679969179,
    "iat": 1679963879,
    "jti": "96c6ad43578d4f30b133ff513a5a2100",
    "user_id": 6,
    "email": "f@f.co"
  }

const authTokens = {}

// const signup = jest.fn();
const loginUser = jest.fn();
const logoutUser = jest.fn();

const AllTheProviders = ({ children }) => {
  return (
    <Router>
      <AuthContext.Provider value={{ user: {}, authTokens, loginUser, logoutUser }}>
        {children}
      </AuthContext.Provider>
    </Router>
  );
};

const customRender = (ui, options) => {
  render(ui, { wrapper: AllTheProviders, ...options });
};

export * from "@testing-library/react";

export default customRender;