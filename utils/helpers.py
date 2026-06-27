def format_response(response, sentiment):
    if sentiment == "negative":
        return "I'm sorry to hear that. " + response
    return response