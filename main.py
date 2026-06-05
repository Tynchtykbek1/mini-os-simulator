from cpu_scheduling import fcfs_schedule, round_robin_schedule, sjf_schedule
from models import Process
from page_replacement import fifo_page_replacement, lru_page_replacement


def copy_processes(processes):
    return [
        Process(
            pid=process.pid,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
        )
        for process in processes
    ]


def create_gantt_chart(processes):
    return [
        (process.pid, process.start_time, process.completion_time)
        for process in processes
    ]


def print_schedule_results(algorithm_name, processes, gantt_chart=None):
    print(f"\n{algorithm_name}")
    print("=" * len(algorithm_name))
    print_gantt_chart(gantt_chart or create_gantt_chart(processes))
    print_process_table(processes)
    print_averages(processes)


def print_gantt_chart(gantt_chart):
    print("Gantt Chart:")
    print(" | ".join(f"P{pid}" for pid, start_time, end_time in gantt_chart))
    print(" ".join(f"{start_time}-{end_time}" for pid, start_time, end_time in gantt_chart))


def print_process_table(processes):
    print("\nProcess Table:")
    print("PID | Arrival | Burst | Start | Completion | Waiting | Turnaround | Response")
    print("-" * 76)

    for process in processes:
        print(
            f"{process.pid:>3} | "
            f"{process.arrival_time:>7} | "
            f"{process.burst_time:>5} | "
            f"{process.start_time:>5} | "
            f"{process.completion_time:>10} | "
            f"{process.waiting_time:>7} | "
            f"{process.turnaround_time:>10} | "
            f"{process.response_time:>8}"
        )


def print_averages(processes):
    total_processes = len(processes)
    average_waiting_time = sum(process.waiting_time for process in processes) / total_processes
    average_turnaround_time = sum(process.turnaround_time for process in processes) / total_processes

    print(f"\nAverage waiting time: {average_waiting_time:.2f}")
    print(f"Average turnaround time: {average_turnaround_time:.2f}")


def print_page_replacement_header(reference_string, number_of_frames):
    print("\nPage Replacement")
    print("================")
    print(f"Reference string: {reference_string}")
    print(f"Number of frames: {number_of_frames}")


def print_page_replacement_results(algorithm_name, result, number_of_frames):
    print(f"\n{algorithm_name} Step-by-Step Table:")
    print("Step | Page | Frames      | Result | Replaced")
    print("-" * 49)

    for step_number, step in enumerate(result["steps"], start=1):
        frames = format_frames(step["frames"], number_of_frames)
        replaced_page = (
            str(step["replaced_page"])
            if step["replaced_page"] is not None
            else "-"
        )

        print(
            f"{step_number:>4} | "
            f"{step['page']:>4} | "
            f"{frames:<11} | "
            f"{step['result']:<6} | "
            f"{replaced_page:>8}"
        )

    print(f"\nTotal page faults: {result['page_faults']}")
    print(f"Total page hits: {result['page_hits']}")


def format_frames(frames, number_of_frames):
    displayed_frames = [str(page) for page in frames]

    while len(displayed_frames) < number_of_frames:
        displayed_frames.append("-")

    return "[" + ", ".join(displayed_frames) + "]"


def main():
    time_quantum = 4
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=2, burst_time=3),
        Process(pid=3, arrival_time=4, burst_time=1),
        Process(pid=4, arrival_time=8, burst_time=2),
    ]

    fcfs_processes = fcfs_schedule(copy_processes(processes))
    sjf_processes = sjf_schedule(copy_processes(processes))
    rr_gantt_chart, rr_processes = round_robin_schedule(
        copy_processes(processes),
        time_quantum,
    )

    print_schedule_results("FCFS Scheduling", fcfs_processes)
    print_schedule_results("SJF Scheduling", sjf_processes)
    print_schedule_results(
        f"Round Robin Scheduling (Time Quantum = {time_quantum})",
        rr_processes,
        rr_gantt_chart,
    )

    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    number_of_frames = 3
    fifo_result = fifo_page_replacement(reference_string, number_of_frames)
    lru_result = lru_page_replacement(reference_string, number_of_frames)

    print_page_replacement_header(reference_string, number_of_frames)
    print_page_replacement_results("FIFO", fifo_result, number_of_frames)
    print_page_replacement_results("LRU", lru_result, number_of_frames)


if __name__ == "__main__":
    main()
