# Lab 2 - Run on Azure

## Prerequisites

```powershell
winget install Microsoft.PowerShell
winget install Git.Git
winget install Python.Python.3.12
python -m pip install --upgrade pip
pip install numpy
```

## Setup

```powershell
git clone https://github.com/sebdanielsson/gik2nx
cd gik2nx/lab2
```

## Run

Each line will return the time it took to run the script in seconds.

```powershell
(Measure-Command { python .\lab2-task1.py }).TotalSeconds
(Measure-Command { python .\lab2-task2.py }).TotalSeconds
(Measure-Command { python .\lab2-task3.py }).TotalSeconds
```
