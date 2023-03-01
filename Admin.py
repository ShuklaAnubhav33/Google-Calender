from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarEventsView(View):
    def get(self, request, *args, **kwargs):
        # Get the credentials from the session or database
        credentials_json = request.session.get('google_calendar_credentials')
        if not credentials_json:
            return HttpResponseBadRequest('Missing Google Calendar credentials')


