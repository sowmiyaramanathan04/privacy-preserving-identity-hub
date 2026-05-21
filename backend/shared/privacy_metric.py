def compute_disclosure_ratio(stored_attributes: int, shared_attributes: int) -> float:
    if stored_attributes == 0:
        return 0.0
    return round(shared_attributes / stored_attributes, 2)
