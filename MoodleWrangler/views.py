from django.shortcuts import render
from django.views.generic import TemplateView
from MoodleWrangler.scraper import load_courses
from MoodleWrangler.credentials import credentials
from MoodleWrangler.authentication import upload_courses


class HomePageView(TemplateView):
    def post(self, request, *args, **kwargs):
        credentials['netname'] = request.POST['netname']
        credentials['password'] = request.POST['password']
        return render(request, 'home.html')

    def get(self, request, *args, **kwargs):
        if request.GET['download_local']:
            load_courses(credentials)
        elif request.GET['download_onedrive']:
            load_courses(credentials)
            upload_courses('downloads')
        return render(request, 'home.html')


class LoginPageView(TemplateView):
    template_name = "login.html"
