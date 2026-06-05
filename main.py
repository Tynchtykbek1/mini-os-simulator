from cpu_scheduling import fcfs_schedule, sjf_schedule
from models import Process


def copy_processes(processes):
    return [
        Process(
            pid=process.pid,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
        )
        for process in processes
    ]


def print_schedule_results(algorithm_name, processes):
    print(f"\n{algorithm_name}")
    print("=" * len(algorithm_name))
    print_gantt_chart(processes)
    print_process_table(processes)
    print_averages(processes)


def print_gantt_chart(processes):
    print("Gantt Chart:")
    print(" | ".join(f"P{process.pid}" for process in processes))
    print(" ".join(f"{process.start_time}-{process.completion_time}" for process in processes))


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


def main():
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=2, burst_time=3),
        Process(pid=3, arrival_time=4, burst_time=1),
        Process(pid=4, arrival_time=8, burst_time=2),
    ]

    fcfs_processes = fcfs_schedule(copy_processes(processes))
    sjf_processes = sjf_schedule(copy_processes(processes))

    print_schedule_results("FCFS Scheduling", fcfs_processes)
    print_schedule_results("SJF Scheduling", sjf_processes)


if __name__ == "__main__":
    main()
