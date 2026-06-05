from cpu_scheduling import fcfs_schedule, round_robin_schedule, sjf_schedule
from models import Process
from page_replacement import (
    fifo_page_replacement,
    lru_page_replacement,
    optimal_page_replacement,
)


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


def run_cpu_scheduling(processes, time_quantum):
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


def run_page_replacement(reference_string, number_of_frames):
    fifo_result = fifo_page_replacement(reference_string, number_of_frames)
    lru_result = lru_page_replacement(reference_string, number_of_frames)
    optimal_result = optimal_page_replacement(reference_string, number_of_frames)

    print_page_replacement_header(reference_string, number_of_frames)
    print_page_replacement_results("FIFO", fifo_result, number_of_frames)
    print_page_replacement_results("LRU", lru_result, number_of_frames)
    print_page_replacement_results("Optimal", optimal_result, number_of_frames)


def run_default_demo():
    time_quantum = 4
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=2, burst_time=3),
        Process(pid=3, arrival_time=4, burst_time=1),
        Process(pid=4, arrival_time=8, burst_time=2),
    ]

    run_cpu_scheduling(processes, time_quantum)

    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    number_of_frames = 3

    run_page_replacement(reference_string, number_of_frames)


def run_custom_cpu_scheduling():
    process_count = read_int("How many processes? ", minimum=1)
    processes = []

    for process_number in range(1, process_count + 1):
        print(f"\nProcess {process_number}")
        pid = read_int("PID: ")
        arrival_time = read_int("arrival_time: ", minimum=0)
        burst_time = read_int("burst_time: ", minimum=1)
        processes.append(Process(pid=pid, arrival_time=arrival_time, burst_time=burst_time))

    time_quantum = read_int("\nRound Robin time quantum: ", minimum=1)
    run_cpu_scheduling(processes, time_quantum)


def run_custom_page_replacement():
    reference_string = read_reference_string()
    number_of_frames = read_int("number_of_frames: ", minimum=1)

    run_page_replacement(reference_string, number_of_frames)


def read_int(prompt, minimum=None):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if minimum is not None and number < minimum:
            print(f"Please enter a number greater than or equal to {minimum}.")
            continue

        return number


def read_reference_string():
    while True:
        value = input("Reference string: ").strip()

        if not value:
            print("Reference string cannot be empty.")
            continue

        try:
            return [int(page) for page in value.split()]
        except ValueError:
            print("Please enter page numbers separated by spaces.")


def print_menu():
    print("\nMini OS Simulator")
    print("=================")
    print("1. Run default demo")
    print("2. Run CPU Scheduling with custom process input")
    print("3. Run Page Replacement with custom input")
    print("4. Exit")


def main():
    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nExiting Mini OS Simulator.")
            break

        if choice == "1":
            run_default_demo()
        elif choice == "2":
            run_custom_cpu_scheduling()
        elif choice == "3":
            run_custom_page_replacement()
        elif choice == "4":
            print("Exiting Mini OS Simulator.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
