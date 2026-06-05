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


def round_robin_schedule(processes, time_quantum):
    if time_quantum <= 0:
        raise ValueError("time_quantum must be greater than 0")

    processes_by_arrival = sorted(processes, key=lambda process: process.arrival_time)
    remaining_time = {
        process.pid: process.burst_time
        for process in processes_by_arrival
    }
    ready_queue = []
    gantt_chart = []
    completed_processes = []
    started_pids = set()
    current_time = 0
    next_process_index = 0

    while len(completed_processes) < len(processes_by_arrival):
        while (
            next_process_index < len(processes_by_arrival)
            and processes_by_arrival[next_process_index].arrival_time <= current_time
        ):
            ready_queue.append(processes_by_arrival[next_process_index])
            next_process_index += 1

        if not ready_queue:
            current_time = processes_by_arrival[next_process_index].arrival_time
            continue

        current_process = ready_queue.pop(0)

        if current_process.pid not in started_pids:
            current_process.start_time = current_time
            current_process.response_time = (
                current_process.start_time - current_process.arrival_time
            )
            started_pids.add(current_process.pid)

        execution_time = min(time_quantum, remaining_time[current_process.pid])
        start_time = current_time
        current_time += execution_time
        remaining_time[current_process.pid] -= execution_time
        gantt_chart.append((current_process.pid, start_time, current_time))

        while (
            next_process_index < len(processes_by_arrival)
            and processes_by_arrival[next_process_index].arrival_time <= current_time
        ):
            ready_queue.append(processes_by_arrival[next_process_index])
            next_process_index += 1

        if remaining_time[current_process.pid] > 0:
            ready_queue.append(current_process)
        else:
            current_process.completion_time = current_time
            current_process.turnaround_time = (
                current_process.completion_time - current_process.arrival_time
            )
            current_process.waiting_time = (
                current_process.turnaround_time - current_process.burst_time
            )
            completed_processes.append(current_process)

    return gantt_chart, completed_processes
