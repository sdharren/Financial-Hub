import React, { useState, useEffect, useRef, useContext } from 'react';
import Chart from "react-apexcharts";
import usePlaid from '../custom_hooks/usePlaid';
import 'chart.js/auto';
import GraphSelect from '../components/GraphSelect';
import useHandleError from '../custom_hooks/useHandleError';
import { lineGraphSizing } from '../static/styling';

function LineGraph({ endpoint, endpoint_parameter, updateGraph, selectOptions, currency}) {
    const [lineChartData, error] = usePlaid({endpoint, endpoint_parameter})
    
    useHandleError(error);

    var chartCategories = [], chartSeries = [];
    for (var key in lineChartData) {
        if ( ! lineChartData.hasOwnProperty(key)) {
            continue;
        }
        chartSeries.push(lineChartData[key].toFixed(2));
        chartCategories.push(key.slice(0, 10));
    }
    console.log(chartSeries)
    let handleSelectionUpdate = async(nextParam) => {
        updateGraph({
            'endpoint': endpoint,
            'param': nextParam
        });
    }

    // Set the options for the chart
    const options = {
        chart: {
            id: 'area-datetime',
            height: 100,
            zoom: {
                autoScaleYaxis: true
            },
        },
        title: {
            text: endpoint_parameter + " " + "Stock Price",
            offsetX: 0,
            offsetY: 0,
            style: {
                color: '#fff',
                fontSize: '12px',
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 600,
                cssClass: 'apexcharts-xaxis-title',
            },
        },
        yaxis: {
            show: true,
            showAlways: true,
            tickAmount: 6,
            labels: {
                formatter: function (value) {
                    return (currency ? currency : '£') + value.toFixed(2);
                },
                show: true,
                align: 'right',
                minWidth: 0,
                maxWidth: 160,
                style: {
                    colors: ['#fff'],
                    fontSize: '12px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 400,
                    cssClass: 'apexcharts-yaxis-label',
                },
                offsetX: 0,
                offsetY: 0,
                rotate: 0,
            },
            axisBorder: {
                show: true,
                color: '#fff',
                offsetX: 0,
                offsetY: 0
            },
        },
            colors: ['#FDD36A'],
            stroke: {
            curve: 'straight',
            },
            xaxis: {
                type: 'datetime',
                categories: chartCategories,
                labels: {
                    style: {
                      colors: '#fff'
                    }
                  }
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                type: 'gradient',
                gradient: {
                    type: 'vertical',
                    shadeIntensity: 0.3,
                    opacityFrom: 0.7,
                    opacityTo: 0.9,
                    stops: [0, 100]
                }
            },
    };
    
        // Set the series data for the chart
        const series = [{
            name: 'Price',
            data: chartSeries,
        }];


      return (
        <div className={lineGraphSizing}>
            {
                selectOptions === undefined || selectOptions === null
                ? null
                : <GraphSelect options={selectOptions} handleSelectionUpdate={handleSelectionUpdate} selectedOption={endpoint_parameter}/>
            }
            {
            lineChartData === null ?
            <p className='text-white'>Loading...</p> :
            <Chart className = 'pt-2' height = "420vh" options={options} series={series} type = "area" />
            }
        </div>
      )
    }


export default LineGraph;
