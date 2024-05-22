class LeavesRules:

    valid_rules = {
        "leave_date_range": "required",
        "leave_type": "required",
        "reason": "required",
    }

    messages = {
        'leave_date_range.required': "Leave Date cannot be empty",
        'leave_type.required': "Leave Type cannot be empty",
        'reason.required': "Please state a reason for this leave",
    }

