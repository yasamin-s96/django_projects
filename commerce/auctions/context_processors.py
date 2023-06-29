def watchlist_processor(request):
    if request.user.is_authenticated:
        return {"watchlist_badge":request.user.watchlist.listings.count()}
    
    else:
        return {"watchlist_badge":0}