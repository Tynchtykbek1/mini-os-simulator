def fcfs_schedule(processes):
    scheduled_processes = sorted(processes, key=lambda process: process.arrival_time)
    current_time = 0

    for process in scheduled_processes:
        # If no process has arrived yet, the CPU stays idle until this process arrives.
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        process.start_time = current_time
        process.completion_time = process.start_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

        current_time = process.completion_time

    return scheduled_processes


def sjf_schedule(processes):
    remaining_processes = list(processes)
    scheduled_processes = []
    current_time = 0

    while remaining_processes:
        arrived_processes = [
            process
            for process in remaining_processes
            if process.arrival_time <= current_time
        ]

        if not arrived_processes:
            current_time = min(process.arrival_time for process in remaining_processes)
            continue

        current_process = min(
            arrived_processes,
            key=lambda process: (process.burst_time, process.arrival_time, process.pid),
        )

        current_process.start_time = current_time
        current_process.completion_time = current_process.start_time + current_process.burst_time
        current_process.turnaround_time = (
            current_process.completion_time - current_process.arrival_time
        )
        current_process.waiting_time = (
            current_process.turnaround_time - current_process.burst_time
        )
        current_process.response_time = (
            current_process.start_time - current_process.arrival_time
        )

        current_time = current_process.completion_time
        scheduled_processes.append(current_process)
        remaining_processes.remove(current_process)

    return scheduled_processes
