
class MetricRules:

    valid_rules = {
        'name': 'required|min:6|max:20|alphanumeric',
        'score': 'required|numeric',
    }

    messages = {
        'required': 'Please input a name',
    }

