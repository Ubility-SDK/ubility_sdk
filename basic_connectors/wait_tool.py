import time
def wait(params):
    """
    Pause the execution for the specified duration.

    :param dict params: Dictionary containing the following keys:
        - duration (float): Duration to wait.
        - durationType (str): Type of duration ("Days", "Hours", "Minutes", "Seconds").

    """
    try:
        if "duration" and "durationType" in params:
            duration = float(params['duration'])
            if duration <= 0:
                raise ValueError("Duration must be a positive number.")
            if params['durationType'] == "Days":
                duration_seconds = duration * 24 * 60 * 60
            elif params['durationType'] == "Hours":
                duration_seconds = duration * 60 * 60
            elif params['durationType'] == "Minutes":
                duration_seconds = duration * 60
            elif params['durationType'] == "Seconds":
                duration_seconds = duration
            else:
                raise ValueError("Invalid duration type.")
            time.sleep(duration_seconds)
            return "Success"
        else:
            raise Exception("Missing Input Data")
    except ValueError as ve:
        raise ValueError(ve)