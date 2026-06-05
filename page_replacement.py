def fifo_page_replacement(reference_string, number_of_frames):
    if number_of_frames <= 0:
        raise ValueError("number_of_frames must be greater than 0")

    frames = []
    page_faults = 0
    page_hits = 0
    steps = []

    for page in reference_string:
        replaced_page = None

        if page in frames:
            page_hits += 1
            result = "Hit"
        else:
            page_faults += 1
            result = "Fault"

            if len(frames) == number_of_frames:
                replaced_page = frames.pop(0)

            frames.append(page)

        steps.append(
            {
                "page": page,
                "frames": frames.copy(),
                "result": result,
                "replaced_page": replaced_page,
            }
        )

    return {
        "steps": steps,
        "page_faults": page_faults,
        "page_hits": page_hits,
    }
