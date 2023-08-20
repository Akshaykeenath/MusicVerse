import datetime

def getClicksDatesInc(clickdata):
    current_date = datetime.date.today()
    dates = []
    clicks = []
    if len(clickdata)>0:
        first_date = clickdata[0]['dates']
        accumulated_clicks = 0  # Variable to accumulate the clicks per day

        # Iterate over the date range from the first date to the current date
        for single_date in range((current_date - first_date).days + 1):
            date = first_date + datetime.timedelta(days=single_date)
            dates.append(date)

            # Check if the date exists in the songclickdata
            clicks_value = next((item['clicks'] for item in clickdata if item['dates'] == date), 0)
            accumulated_clicks += clicks_value  # Accumulate the clicks per day
            clicks.append(accumulated_clicks)

    return clicks, dates

def getClicksDates(songclickdata):
    current_date = datetime.date.today()
    first_date = songclickdata[0]['dates']
    
    dates = []
    clicks = []

    # Iterate over the date range from the first date to the current date
    for single_date in range((current_date - first_date).days + 1):
        date = first_date + datetime.timedelta(days=single_date)
        dates.append(date)

        # Check if the date exists in the songclickdata
        clicks_value = next((item['clicks'] for item in songclickdata if item['dates'] == date), 0)
        clicks.append(clicks_value)

    return clicks, dates

def getClicksLikesDates(clickdata, songlikes):
    # Determine the oldest date from clickdata and songlikes
    clickdata_dates = {item['dates'] for item in clickdata}
    songlikes_dates = {item['dates'] for item in songlikes}
    all_dates = clickdata_dates.union(songlikes_dates)
    dates = []
    clicks = []
    likes = []
    if bool(all_dates):
        first_date = min(all_dates)
        current_date = datetime.date.today()
        accumulated_clicks = 0  # Variable to accumulate the clicks per day
        accumulated_likes = 0  # Variable to accumulate the likes per day

        # Iterate over the date range from the first date to the current date
        for single_date in range((current_date - first_date).days + 1):
            date = first_date + datetime.timedelta(days=single_date)
            dates.append(date)

            # Check if the date exists in clickdata
            clicks_value = next((item['clicks'] for item in clickdata if item['dates'] == date), 0)
            accumulated_clicks += clicks_value  # Accumulate the clicks per day
            clicks.append(accumulated_clicks)

            # Check if the date exists in songlikes
            likes_value = next((item['likes'] for item in songlikes if item['dates'] == date), 0)
            accumulated_likes += likes_value  # Accumulate the likes per day
            likes.append(accumulated_likes)
    
    return clicks, likes, dates