from src.common.llm.model_strategy import get_model_strategy


def _normalize_messages(input_data):
    if input_data is None:
        return []

    if isinstance(input_data, str):
        return [{"role": "user", "content": input_data}]

    if not isinstance(input_data, (list, tuple)):
        raise TypeError("Chat input must be a string or a list of message dicts.")

    normalized = []
    for message in input_data:
        if not isinstance(message, dict):
            raise TypeError("Each message must be a dictionary with 'role' and 'content'.")

        role = str(message.get("role", "user")).lower()
        if role not in {"user", "assistant", "system"}:
            role = "user"

        normalized.append({
            "role": role,
            "content": str(message.get("content", "")),
        })

    return normalized


def invoke(input, history=None, provider=None):
    if history is not None:
        messages = _normalize_messages(history)
        if isinstance(input, str):
            messages.append({"role": "user", "content": input})
        else:
            messages = _normalize_messages(input)
    else:
        messages = _normalize_messages(input)

    if not messages:
        return ""

    payload = [{"role": "system", "content": "You are a helpful AI assistant."}, *messages]
    model = get_model_strategy(provider)
    return model.invoke(payload)


if __name__ == "__main__":
    invoke("hello")