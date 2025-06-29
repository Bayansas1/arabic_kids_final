
def update_bkt(p_know, p_transit, p_guess, p_slip, is_correct):
    # حساب احتمالية المعرفة بناءً على الإجابة
    if is_correct:
        num = p_know * (1 - p_slip)
        denom = num + (1 - p_know) * p_guess
    else:
        num = p_know * p_slip
        denom = num + (1 - p_know) * (1 - p_guess)

    p_know_given_obs = num / denom

    # احتمال الانتقال (التعلم) بعد المحاولة
    p_know_next = p_know_given_obs + (1 - p_know_given_obs) * p_transit

    return p_know_next
