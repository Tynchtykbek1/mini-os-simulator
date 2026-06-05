# Mini OS Simulator

A small Python project for demonstrating Operating Systems concepts.

## Implemented Features

- FCFS (First-Come, First-Served) CPU Scheduling
- SJF (Shortest Job First) CPU Scheduling

## Files

- `models.py`: contains the `Process` model.
- `cpu_scheduling.py`: contains the FCFS and SJF scheduling algorithms.
- `main.py`: creates sample processes, runs the scheduling algorithms, and prints results.

## Shortest Job First

SJF chooses the arrived process with the smallest burst time. This project uses
non-preemptive SJF, so once a process starts running, it keeps the CPU until it
finishes.

## Run

```bash
python main.py
```
