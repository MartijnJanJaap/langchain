class ShouldContinueNode:
    def __init__(self, max_iterations=5):
        self.max_iterations = max_iterations

    def __call__(self, state):
        messages = state.get("messages", [])
        attempts = len([m for m in messages if m["role"] in ("programmer", "reviser")])

        print(f"[ShouldContinueNode] Attempt count: {attempts}")

        if attempts >= self.max_iterations:
            print("[ShouldContinueNode] Maximum attempts reached. Asking user for next instruction.")
            return {
                **state,
                "should_continue": False
            }

        print("[ShouldContinueNode] Continuing automatically.")
        return {
            **state,
            "should_continue": True
        }