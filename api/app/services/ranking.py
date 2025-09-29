def quality_score(source: str, content_length: int) -> float:
    """Simple quality scoring based on source and content length"""
    base_score = 0.5
    
    # Source quality multipliers
    source_scores = {
        "mdn": 1.0,
        "github": 0.9,
        "stackoverflow": 0.8,
        "wikipedia": 0.9,
        "official": 1.0,
        "manual": 0.7,
        "seed": 0.8
    }
    
    source_multiplier = source_scores.get(source.lower(), 0.6)
    
    # Content length bonus (more content = higher quality, up to a point)
    length_bonus = min(content_length / 1000, 0.3)  # Max 0.3 bonus for 1000+ chars
    
    return min(base_score * source_multiplier + length_bonus, 1.0)
