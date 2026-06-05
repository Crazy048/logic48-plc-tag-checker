# Logic48 PLC Tag Checker

A lightweight open-source CLI tool for validating PLC/HMI/SCADA tag lists.

The project helps automation engineers improve the quality of industrial automation documentation by checking tag names, data types, addresses, descriptions, and duplicated entries before importing or using tag lists in PLC, HMI, or SCADA projects.

## Why this project exists

Small and medium industrial automation projects often suffer from inconsistent tag naming, missing descriptions, duplicated addresses, and poorly documented PLC/HMI variables.

This tool provides a simple automated check for tag lists exported from engineering workflows or prepared for PLC/HMI/SCADA projects.

## Features

- Validate CSV tag lists
- Detect duplicated tag names
- Detect duplicated addresses
- Detect missing descriptions
- Detect unsupported data types
- Detect suspiciously short descriptions
- Check basic naming convention
- Generate a Markdown quality report

## Example CSV format

```csv
name,type,address,description,area
Pump_101_Start,Bool,%M0.0,Start command for pump 101,OilStation
Pump_101_RunFb,Bool,%I0.0,Run feedback from pump 101,OilStation
Tank_101_Level,Real,%MD10,Tank 101 level,OilStation
