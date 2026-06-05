from flask import Flask, render_template, request

from cpu_scheduling import fcfs_schedule, round_robin_schedule, sjf_schedule
from models import Process
from page_replacement import (
    fifo_page_replacement,
    lru_page_replacement,
    optimal_page_replacement,
)


app = Flask(__name__)


DEFAULT_PROCESSES_TEXT = "1 0 5\n2 2 3\n3 4 1\n4 8 2"
DEFAULT_TIME_QUANTUM = "4"
DEFAULT_REFERENCE_STRING = "7 0 1 2 0 3 0 4 2 3 0 3 2"
DEFAULT_NUMBER_OF_FRAMES = "3"


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
        {
            "pid": process.pid,
            "start_time": process.start_time,
            "end_time": process.completion_time,
        }
        for process in processes
    ]


def calculate_averages(processes):
    return {
        "waiting_time": sum(process.waiting_time for process in processes) / len(processes),
        "turnaround_time": (
            sum(process.turnaround_time for process in processes) / len(processes)
        ),
    }


def build_cpu_result(name, processes, gantt_chart=None):
    return {
        "name": name,
        "gantt_chart": gantt_chart or create_gantt_chart(processes),
        "processes": processes,
        "averages": calculate_averages(processes),
    }


def run_cpu_scheduling(processes, time_quantum):
    fcfs_processes = fcfs_schedule(copy_processes(processes))
    sjf_processes = sjf_schedule(copy_processes(processes))
    rr_gantt_chart, rr_processes = round_robin_schedule(
        copy_processes(processes),
        time_quantum,
    )

    return [
        build_cpu_result("FCFS Scheduling", fcfs_processes),
        build_cpu_result("SJF Scheduling", sjf_processes),
        build_cpu_result(
            f"Round Robin Scheduling (Time Quantum = {time_quantum})",
            rr_processes,
            [
                {"pid": pid, "start_time": start_time, "end_time": end_time}
                for pid, start_time, end_time in rr_gantt_chart
            ],
        ),
    ]


def run_page_replacement(reference_string, number_of_frames):
    return [
        {
            "name": "FIFO",
            "result": fifo_page_replacement(reference_string, number_of_frames),
        },
        {
            "name": "LRU",
            "result": lru_page_replacement(reference_string, number_of_frames),
        },
        {
            "name": "Optimal",
            "result": optimal_page_replacement(reference_string, number_of_frames),
        },
    ]


def parse_processes(processes_text):
    if not processes_text.strip():
        raise ValueError("Process input cannot be empty.")

    processes = []

    for line_number, line in enumerate(processes_text.splitlines(), start=1):
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) != 3:
            raise ValueError(
                f"Line {line_number} must contain exactly 3 integers: "
                "pid arrival_time burst_time."
            )

        try:
            pid, arrival_time, burst_time = [int(part) for part in parts]
        except ValueError as error:
            raise ValueError(f"Line {line_number} must contain only integers.") from error

        if arrival_time < 0:
            raise ValueError(f"Line {line_number}: arrival_time must be >= 0.")
        if burst_time <= 0:
            raise ValueError(f"Line {line_number}: burst_time must be > 0.")

        processes.append(
            Process(pid=pid, arrival_time=arrival_time, burst_time=burst_time)
        )

    if not processes:
        raise ValueError("Process input cannot be empty.")

    return processes


def parse_positive_int(value, field_name):
    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be an integer.") from error

    if number <= 0:
        raise ValueError(f"{field_name} must be > 0.")

    return number


def parse_reference_string(reference_text):
    if not reference_text.strip():
        raise ValueError("Reference string cannot be empty.")

    try:
        return [int(page) for page in reference_text.split()]
    except ValueError as error:
        raise ValueError("Reference string must contain only integers.") from error


@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "processes_text": DEFAULT_PROCESSES_TEXT,
        "time_quantum": DEFAULT_TIME_QUANTUM,
        "reference_string": DEFAULT_REFERENCE_STRING,
        "number_of_frames": DEFAULT_NUMBER_OF_FRAMES,
        "cpu_results": None,
        "page_results": None,
        "cpu_error": None,
        "page_error": None,
    }

    if request.method == "POST":
        context["processes_text"] = request.form.get(
            "processes_text",
            DEFAULT_PROCESSES_TEXT,
        )
        context["time_quantum"] = request.form.get(
            "time_quantum",
            DEFAULT_TIME_QUANTUM,
        )
        context["reference_string"] = request.form.get(
            "reference_string",
            DEFAULT_REFERENCE_STRING,
        )
        context["number_of_frames"] = request.form.get(
            "number_of_frames",
            DEFAULT_NUMBER_OF_FRAMES,
        )

        form_type = request.form.get("form_type")

        if form_type == "cpu":
            try:
                processes = parse_processes(context["processes_text"])
                time_quantum = parse_positive_int(
                    context["time_quantum"],
                    "Time quantum",
                )
                context["cpu_results"] = run_cpu_scheduling(processes, time_quantum)
            except ValueError as error:
                context["cpu_error"] = str(error)

        if form_type == "page":
            try:
                reference_string = parse_reference_string(context["reference_string"])
                number_of_frames = parse_positive_int(
                    context["number_of_frames"],
                    "Number of frames",
                )
                context["page_results"] = run_page_replacement(
                    reference_string,
                    number_of_frames,
                )
                context["parsed_reference_string"] = reference_string
            except ValueError as error:
                context["page_error"] = str(error)

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
