"""twitterNosql URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from twitter import views, csv_importer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^userInfo', views.userInfo),
    url(r'^tweet/new', views.newTweet),
    url(r'^timeline', views.timeline),
    url(r'^trends', views.trends),
    url(r'^follow', views.follow),
    url(r'^unfollow', views.unfollow),
    url(r'^getFollowers', views.followers),
    url(r'^getFollowings', views.followings),
    url(r'^search/users', views.searchUsers),
    url(r'^search/hashtags', views.searchHashtags),
    url(r'^retweet', views.retweet),
    url(r'^profile', views.profile),
    url(r'^like', views.like),
    url(r'^logs', views.logs),

    url(r'^import/users', csv_importer.users),
    url(r'^import/tweets', csv_importer.tweets),
    url(r'^import/follow', csv_importer.follow),
    url(r'^import/retweet', csv_importer.retweet),

]
