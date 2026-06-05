from dataclasses import dataclass


@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    start_time: int = 0
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = 0
