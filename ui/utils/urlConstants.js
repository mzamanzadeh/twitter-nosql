var app = angular.module("app");
var apiUrl = "http://localhost:8000/";
app.constant("UrlConstants", {
    login: apiUrl + "login",
    register: apiUrl + "register",
    userInfo: apiUrl + "userInfo",
    tweet: apiUrl + "tweet/new",
    myTweets: apiUrl + "tweet/my",
    trends: apiUrl + "trends",
    searchUsers: apiUrl + "search/users",
    searchHashtags: apiUrl + "search/hashtags",
    follow: apiUrl + "follow",
    unfollow: apiUrl + "unfollow",
    timeline: apiUrl + "timeline",
    retweet: apiUrl + "retweet",
    like: apiUrl + "like",
    profile: apiUrl + "profile",
    followers: apiUrl + "getFollowers",
    followings: apiUrl + "getFollowings",
    logs: apiUrl + "logs"
});