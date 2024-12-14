#!/bin/bash

# Initialize the Airflow database
airflow db init

# Start the scheduler and webserver
airflow scheduler & airflow webserver
