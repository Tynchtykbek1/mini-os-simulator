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


def lru_page_replacement(reference_string, number_of_frames):
    if number_of_frames <= 0:
        raise ValueError("number_of_frames must be greater than 0")

    frames = []
    last_used = {}
    page_faults = 0
    page_hits = 0
    steps = []

    for current_index, page in enumerate(reference_string):
        replaced_page = None

        if page in frames:
            page_hits += 1
            result = "Hit"
        else:
            page_faults += 1
            result = "Fault"

            if len(frames) == number_of_frames:
                replaced_page = min(frames, key=lambda frame_page: last_used[frame_page])
                frames.remove(replaced_page)
                del last_used[replaced_page]

            frames.append(page)

        last_used[page] = current_index

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


def optimal_page_replacement(reference_string, number_of_frames):
    if number_of_frames <= 0:
        raise ValueError("number_of_frames must be greater than 0")

    frames = []
    page_faults = 0
    page_hits = 0
    steps = []

    for current_index, page in enumerate(reference_string):
        replaced_page = None

        if page in frames:
            page_hits += 1
            result = "Hit"
        else:
            page_faults += 1
            result = "Fault"

            if len(frames) == number_of_frames:
                future_references = reference_string[current_index + 1:]
                replaced_page = find_optimal_page_to_replace(frames, future_references)
                frames.remove(replaced_page)

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


def find_optimal_page_to_replace(frames, future_references):
    farthest_use_index = -1
    page_to_replace = frames[0]

    for page in frames:
        if page not in future_references:
            return page

        next_use_index = future_references.index(page)
        if next_use_index > farthest_use_index:
            farthest_use_index = next_use_index
            page_to_replace = page

    return page_to_replace
