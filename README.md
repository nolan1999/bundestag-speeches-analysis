# Bundestag speeches analysis

This repository contains the data, code, and report for a project for the Data Literacy course (WS21/22) at University of Tübingen.

Find the report [here](report/report.pdf).

**Repo structure**:  
 - data: functions to download the data via api, functions to preprocess the data. Running get_data.py is all you need to do.
 - experiments: the analyses we performed. For each experiment, params.py defines the parameters for features building, topics extraction, and sentiments extraction. .ipynb notebooks contain the analyses. expxx.py is the script to run featurization, topic extraction, and sentiment extraction. The final analysis is contained in expfinal, but we keep all work for completeness.
 - interpretation: contains our attempts to interpret the results.
 - models: utility functions for the models trained (topic extraction and sentiment detection).
 - report: the latex project for the final report.


To run an experiment: python -m experiments.exp--.exp--
