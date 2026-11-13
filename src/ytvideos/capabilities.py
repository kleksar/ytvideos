"""Keep an absent runtime observation distinct from observed unavailability."""


def observation_state(observation):
    if (not isinstance(observation, dict) or type(observation.get("available")) is not bool
            or not observation.get("evidence")):
        return "unobserved"
    return "available" if observation["available"] else "unavailable"


def capability_check(name, observation):
    state = observation_state(observation)
    details = observation if isinstance(observation, dict) else {}
    result = {**details, "capability": name, "state": state,
              "available": None if state == "unobserved" else state == "available",
              "evidence": details.get("evidence") or "No verified observation in this run."}
    if state == "unobserved":
        result["next_action"] = (
            "Inspect the tools exposed to the current host/session, including deferred tool discovery. "
            "Record actual availability and evidence with capabilities, then retry next. "
            "This missing observation is not an environmental blocker.")
    elif state == "unavailable":
        result["next_action"] = "Use the observed failure to repair this capability; continue independent tasks."
    return result
