def validate_rating(request):
    rating = request.json_body['rating']
    if 0 < rating <= 5:
        return rating
    return False
