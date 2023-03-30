import React from 'react';
import { getAllByTitle, getByLabelText, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom'; 
import Navbar from '../../components/Navbar';
import { customRenderUser, customRenderNoUser } from '../test-utils'

describe('Navbar with user', () => {
    it("renders without crashing", () => {
        customRenderUser(<Navbar />)
    })

    it("renders site title", () => {
        customRenderUser(<Navbar />)

        const siteTitle = screen.getByRole('img', {name : 'logo'})
        expect(siteTitle).toBeInTheDocument()
    })

    it("renders correct amount of 'list items' items", () => {
        customRenderUser(<Navbar />)

        const li_items = screen.getAllByRole('listitem')
        expect(li_items.length).toBe(4)
    })

    it('renders "link assets", "manage linked assets" and "My account"', () => {
        customRenderUser(<Navbar />)

        const linkAssets = screen.getByText('Link assets')
        const manageAssets = screen.getByText('Manage linked assets')
        const myAccount = screen.getByText('My account')

        expect(linkAssets).toBeInTheDocument()
        expect(manageAssets).toBeInTheDocument()
        expect(myAccount).toBeInTheDocument()
    })
})

describe('Navbar with no user', () => {
    it("renders without crashing", () => {
        customRenderNoUser(<Navbar />)
    })

    it("renders site title", () => {
        customRenderNoUser(<Navbar />)

        const siteTitle = screen.getByRole('img', {name : 'logo'})
        expect(siteTitle).toBeInTheDocument()
    })

    it("renders correct amount of 'list items' items", () => {
        customRenderNoUser(<Navbar />)

        const li_items = screen.getAllByRole('listitem')
        expect(li_items.length).toBe(3)
    })

    it('renders "about", "sign up" and "log in"', () => {
        customRenderNoUser(<Navbar />)

        const login = screen.getByText('Log in')
        const signup = screen.getByText('Sign up')
        const about = screen.getByText('About')

        expect(login).toBeInTheDocument()
        expect(signup).toBeInTheDocument()
        expect(about).toBeInTheDocument()
    })

})