import React, { useState, useEffect, useRef, useContext } from 'react';
import 'chart.js/auto';
import Chart from "react-apexcharts";
import AuthContext from '../context/AuthContext';
import { prototype } from 'apexcharts';

function LineGraph() {
    const data =  {
        '2023-02-10T00:00:00-05:00': 28.100000381469727, 
        '2023-02-13T00:00:00-05:00': 28.549999237060547, 
        '2023-02-14T00:00:00-05:00': 28.309999465942383, 
        '2023-02-15T00:00:00-05:00': 28.530000686645508, 
        '2023-02-16T00:00:00-05:00': 28.639999389648438, 
        '2023-02-17T00:00:00-05:00': 28.690000534057617, 
        '2023-02-21T00:00:00-05:00': 28.209999084472656, 
        '2023-02-22T00:00:00-05:00': 28.200000762939453, 
        '2023-02-23T00:00:00-05:00': 28.549999237060547, 
        '2023-02-24T00:00:00-05:00': 27.690000534057617, 
        '2023-02-27T00:00:00-05:00': 27.639999389648438, 
        '2023-02-28T00:00:00-05:00': 27.270000457763672, 
        '2023-03-01T00:00:00-05:00': 27.489999771118164, 
        '2023-03-02T00:00:00-05:00': 27.059999465942383, 
        '2023-03-03T00:00:00-05:00': 27.25, 
        '2023-03-06T00:00:00-05:00': 27.68000030517578, 
        '2023-03-07T00:00:00-05:00': 27.34000015258789, 
        '2023-03-08T00:00:00-05:00': 28.190000534057617, 
        '2023-03-09T00:00:00-05:00': 27.709999084472656
        };

        var chartCategories = [], chartSeries = [];
        for (var key in data) {
            if ( ! data.hasOwnProperty(key)) {
                continue;
             }
             chartSeries.push(data[key]);
             chartCategories.push(key);
        }

        // Set the options for the chart
        const options = {
            chart: {
                id: 'area-chart'
            },
            xaxis: {
                categories: chartCategories,
            }
        };

        // Set the series data for the chart
        const series = [{
            name: 'Price',
            data: chartSeries,
        }];

        // Return the Chart component with the options and series
        return <Chart options={options} series={series} type="area" height={350} />
}

export default LineGraph;
