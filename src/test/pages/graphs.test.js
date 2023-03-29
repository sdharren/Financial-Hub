import React from 'react';
import { render, screen } from '@testing-library/react';
import BalancesDisplay from '../../pages/BalancesDisplay';
import RecentTransactions from '../../dashboard_components/RecentTransactionsDisplay';
import CurrencyDisplay from '../../pages/CurrencyDisplay';
import BarChart from '../../pages/TransactionDisplay';
import BarChartDisplay from '../../pages/SectorSpendingDisplay';
import InvestmentGraphs from '../../pages/InvestmentGraphs';
import { customRenderUser } from '../test-utils'

describe("Balances Display", () => {
    it("renders without crashing", () => {
        customRenderUser(<BalancesDisplay />)
    })
})

describe("Recent transactions table", () => {
    it("renders without crashing", () => {
        customRenderUser(<RecentTransactions />)
    })
})

describe("Curreny Display", () => {
    it("renders without crashing", () => {
        customRenderUser(<CurrencyDisplay />)
    })
})

describe("Spending habits bar chart", () => {
    it("renders without crashing", () => {
        customRenderUser(<BarChart />)
    })
})

describe("Sector spending bar chart", () => {
    it("renders without crashing", () => {
        customRenderUser(<BarChartDisplay />)
    })
})

describe("Investment graphs display", () => {
    it("renders without crashing", () => {
        customRenderUser(<InvestmentGraphs />)
    })
})