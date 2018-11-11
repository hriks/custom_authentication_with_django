"""Here we are using custom login so i have commented out admin login url
"""
from django.conf.urls import url
# from django.contrib import admin
from users.views import LoginPage, Home, Logout, Register


urlpatterns = [
    url(r'^home', Home.as_view(), name="home"),
    url(r'^logout', Logout.as_view(), name="logout"),
    url(r'^register', Register.as_view(), name="register"),
    url(r'^', LoginPage.as_view(), name="loginPage"),
]
