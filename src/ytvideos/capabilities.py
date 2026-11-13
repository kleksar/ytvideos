"""Keep an absent runtime observation distinct from observed unavailability."""


DISCOVERY = {
    "sessions.independent": (
        "Inspect directly exposed agent/session tools as well as deferred tool registries. "
        "If collaboration.spawn_agent or spawn_agent is exposed, it supplies a fresh independent reviewer; "
        "it need not be listed in ALL_TOOLS or be named 'reviewer'. Use a fresh context, pass the exact artifact "
        "without the author's verdict, and retain the returned review/session evidence. "
        "Temporary session capacity is a scheduling condition: finish or wait for active work, then retry. "
        "Record unavailable only after an actual supported-host error or a complete tool inventory."),
    "web.search": (
        "Inspect the current host's directly exposed public web search tools and deferred search registry. "
        "Use an actual search/open result as evidence; missing saved observations do not mean search is absent."),
}


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
    if name in DISCOVERY:
        result["discovery"] = DISCOVERY[name]
    if state == "unobserved":
        result["next_action"] = (
            "Inspect the tools exposed to the current host/session, including deferred tool discovery. "
            "Record actual availability and evidence with capabilities, then retry next. "
            "This missing observation is not an environmental blocker.")
    elif state == "unavailable":
        result["next_action"] = "Use the observed failure to repair this capability; continue independent tasks."
    return result
