from django.shortcuts import render
from django.http import JsonResponse
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from oauth2client import file, client


# @login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def add_meal(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    # payload = {
    #     "access_token": social.extra_data["access_token"],
        # "refresh_token": social.extra_data["refresh_token"],
        # "token_uri": social.extra_data["token_uri"],
    # }
    credentials = client.AccessTokenCredentials(access_token, 'eudaemo')

    year = '2019'
    month = '3'
    day = '28'

    GMT_OFF = '-07:00'
    EVENT = {
        'summary': "doing the other thing",
        'start': {'dateTime': year+"-"+month+"-"+day+'T20:00:00%s' % GMT_OFF},
        'end': {'dateTime': year+"-"+month+"-"+day+'T20:30:00%s' % GMT_OFF},
        'description': 'three eggs, \n pepper, salt, butter, olive oil, beans, cumin, oranges, peanut butter, crushed red pepper, asparagus'
    }

    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId='primary', body=EVENT).execute()
    print(event)
    return render(request, 'core/home.html')
    # return JsonResponse({"access_token": social.extra_data['access_token']})


