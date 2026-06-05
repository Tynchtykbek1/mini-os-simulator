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
