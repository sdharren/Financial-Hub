import React, { useContext } from "react";
import { render, screen} from "@testing-library/react";
import userEvent from '@testing-library/user-event'
import Dashboard from "../../pages/Dashboard";
import {customRenderUser} from "../test-utils";

describe("Dashboard", () => {
    it('renders without crashing', () => {
        customRenderUser(
            <Dashboard />
        )
        screen.debug()
    })

    it("renders correct number of categories", () => {
        customRenderUser(
            <Dashboard />
        )

        const chartTabs = screen.getByTestId('graph-tabs').querySelectorAll(".piechart-tab")
        expect(chartTabs.length).toBe(4)
    })

    it("Overall has 1 tab", () => {
        customRenderUser(
            <Dashboard />
        )
        
        const overallTab = screen.getByText('Overall')
        userEvent.click(overallTab)
        const chartTabs = screen.getByTestId('graph-names').querySelectorAll(".piechart-graph")
        expect(chartTabs.length).toBe(1)
    })

    it("Banks has 5 tabs", () => {
        customRenderUser(
            <Dashboard />
        )
        
        const banksTab = screen.getByText('Banks')
        userEvent.click(banksTab)
        const chartTabs = screen.getByTestId('graph-names').querySelectorAll(".piechart-graph")
        expect(chartTabs.length).toBe(5)
    })

    it("Stocks has 4 tabs", () => {
        customRenderUser(
            <Dashboard />
        )
        
        const stocksTab = screen.getByText('Stocks')
        userEvent.click(stocksTab)
        const chartTabs = screen.getByTestId('graph-names').querySelectorAll(".tablinks")
        expect(chartTabs.length).toBe(4)
    })
})