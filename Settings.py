GOOGLE_OAUTH2_CLIENT_CONFIG = {
    'web': {
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET',
        'redirect_uris': ['http://localhost:8000/rest/v1/calendar/redirect/'],
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'userinfo_uri': 'https://www.googleapis.com/oauth2/v1/userinfo',
        'scope': '

