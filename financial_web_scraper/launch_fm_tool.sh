#!/usr/bin/env bash

# set -x # Set all executed commands to be output to console

SCRIPT=${BASH_SOURCE[0]}

function usage()
{
    echo "this script will launch the financial modelling tool and provide an excel output with company valuations"
    echo "USAGE   : launch_fm_tool.sh <ticker_name> <historical_data_number_of_years>"
    echo "EXAMPLE : ./launch_fm_tool.sh 'AAPL' 5"
    echo ""
    echo "MANDATORY ARGUMENTS"
    echo " <ticker_name>                      -- Stock ticker to pull data and calculate results on"
    echo " <historical_data_number_of_years>  -- Number of years of historical data to use"
    echo ""
}

if [ $# -lt 1 ]
then
	usage
	exit 1
fi

if [[ $1 == "-h" ||$1 == "--help" ]]
then
	usage
	exit 0
fi

TICKER_NAME=$1
HISTORICAL_DATA_NUMBER_OF_YEARS=$2
OPERATING_PERFORMANCE_METRIC=${3:-"Unlevered Free Cash Flow"}

echo "Running ${SCRIPT}"
echo "Grabbing Stock Data for ${TICKER_NAME}"
echo "Retreiving ${HISTORICAL_DATA_NUMBER_OF_YEARS} years of data"
echo "Using ${OPERATING_PERFORMANCE_METRIC} to complete financial analysis"
