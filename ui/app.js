var app = angular.module("app",
    [
        "ui.bootstrap",
        "ui.bootstrap.tpls",
        "ui.router",
        "toastr",
        "ngCookies"
    ]);

app.config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state("home", {
            url: "/home",
            params: {
                logout: false
            },
            controller: "homeCtrl",
            controllerAs: "vm",
            templateUrl: "pages/home/home.html"
        })
        .state("login", {
            url: "/login",
            controller: "loginCtrl",
            controllerAs: "vm",
            templateUrl: "pages/login/login.html"
        })
        .state("register", {
            url: "/register",
            controller: "registerCtrl",
            controllerAs: "vm",
            templateUrl: "pages/register/register.html"
        })
        .state("profile", {
            url: "/profile/:username",
            controller: "profileCtrl",
            controllerAs: "vm",
            templateUrl: "pages/profile/profile.html"
        })
        .state("tag", {
            url: "/tag/:tagName",
            params: {
                tag: true
            },
            controller: "tagCtrl",
            controllerAs: "vm",
            templateUrl: "pages/home/home.html"
        })
        .state("search", {
            url: "/search/:query",
            params: {
                search: true
            },
            controller: "searchCtrl",
            controllerAs: "vm",
            templateUrl: "pages/home/home.html"
        })
        .state("trends", {
            url: "/trends",
            controller: "trendsCtrl",
            controllerAs: "vm",
            templateUrl: "pages/trend/trend.html"
        })
        .state("myProfile", {
            url: "/me",
            controller: "meCtrl",
            controllerAs: "vm",
            templateUrl: "pages/profile/profile.html"
        })
        .state("users", {
            url: "/users/:query",
            controller: "usersCtrl",
            controllerAs: "vm",
            templateUrl: "pages/home/home.html"
        });
    $urlRouterProvider.otherwise('/home');
});
app.service('authInterceptor', function ($q, $rootScope) {
    var service = this;

    service.responseError = function (response) {
        if (response.status > 400 && response.status < 500) {
            $rootScope.$emit('unauthorized');
        }
        return $q.reject(response);
    };
});
app.run(function ($rootScope, Notify, $state, $cookies, $http, $sce, UrlConstants, $uibModal) {
    $rootScope.getUserInfo = function () {
        return $http.get(UrlConstants.userInfo).success(function (response) {
            $rootScope.loggedIn = true;
            $rootScope.myData = response;
        }).error(function () {
            $cookies.remove("token");
            $http.defaults.headers.common['Authorization'] = "";
        })
    };

    function init() {
        if ($cookies.get("token")) {
            var token = $cookies.get("token");
            $http.defaults.headers.common['Authorization'] = token;
            $rootScope.getUserInfo();
        }
    }

    $rootScope.searchFormData = {};
    $rootScope.tagModeSearch = false;
    $rootScope.$on("unauthorized", function () {
        Notify.warning("Unauthorized.", "You Do Not Own The Right Authorization to Access That Content, Please Login or Signup ASAP");
    });
    $rootScope.openNewPostModal = function () {
        $uibModal.open({
            templateUrl: 'pages/includes/modals/newPost.html',
            controller: function ($http, UrlConstants, $uibModalInstance, $scope) {
                var mc = this;
                mc.formData = {};
                mc.hashtags = [];
                mc.contentLength = 0;
                mc.cancel = function () {
                    $uibModalInstance.dismiss();
                };
                mc.send = function () {
                    if (mc.formData.tweet) {
                        $http.post(UrlConstants.tweet, mc.formData).success(function (response) {
                            mc.cancel();
                            Notify.success("Successful!", "Your Tweet is Now Available.");
                        }).error(function () {

                        })
                    }
                };
                $scope.$watch("mc.formData.tweet.length", function () {
                    mc.hashtags = [];
                    if (mc.formData.tweet === null || mc.formData.tweet === undefined) {
                        mc.contentLength = 0;
                        mc.hashtags = [];
                    } else {
                        var hashtags = mc.formData.tweet.match(/(#[a-z0-9][a-z0-9\-_]*)/ig);
                        angular.forEach(hashtags, function (str) {
                            if (mc.hashtags.indexOf(str) < 0) {
                                mc.hashtags.push(str);
                            }
                        });
                        mc.contentLength = mc.formData.tweet.length;
                    }
                })
            },
            controllerAs: 'mc',
            size: 'lg'
        })
    };
    $rootScope.globalSearch = function () {
        if ($rootScope.searchFormData.query)
            switch ($rootScope.tagModeSearch) {
                case 1: {
                    $state.go("tag", {tagName: $rootScope.searchFormData.query});
                    closeSearchBox();
                }
                    break;
                case 0: {
                    $state.go("search", {query: $rootScope.searchFormData.query});
                    closeSearchBox();
                }
                    break;
                case -1: {
                    $state.go("users", {query: $rootScope.searchFormData.query})
                    closeSearchBox();
                }
            }
        else {
            Notify.error("Error", "Please Fill Search Input");
        }
    };
    $rootScope.followUser = function (username) {
        $http.post(UrlConstants.follow, {
            username: username
        }).success(function (response) {
            Notify.success("Succes", "You Followed " + username);
        })
    };
    $rootScope.unfollowUser = function (username) {
        $http.post(UrlConstants.unfollow, {
            username: username
        }).success(function (response) {
            Notify.success("Succes", "You Unollowed " + username);
        })
    };
    $rootScope.goToTag = function (tag) {
        if (tag.indexOf("#") < 0) {
            $state.go("tag", {tagName: tag});
        } else {
            $state.go("tag", {tagName: tag.replace("#", "")})
        }
    };
    $rootScope.retweet = function (tweet) {
        $http.post(UrlConstants.retweet, {
            key: tweet.key
        }).success(function (response) {
            Notify.success("Success", "You Retweeted That!");
        })
    };
    $rootScope.like = function (tweet) {
        if (!tweet.isLiked) {
            $http.post(UrlConstants.like, {
                key: tweet.key
            }).success(function (response) {
                Notify.success("Success", "You Liked That!");
                tweet.isLiked = true;
                tweet.likes++;
            }).error(function (response, status) {
                if (status === 400) {
                    tweet.isLiked = true;
                    Notify.info("OH!", "You Have Already Liked That!")
                }
            })
        } else {
            Notify.info("OH!", "You Have Already Liked That!")
        }
    };
    $rootScope.countRetweets = function (tweets) {
        var count = 0;
        angular.forEach(tweets, function (tweet) {
                if (tweet.retweetedFrom) {
                    count++;
                }
            }
        );
        return count;
    };
    $rootScope.processTweets = function (tweets) {
        angular.forEach(tweets, function (tweet) {
            // TWEET TEXT
            if (tweet.text) {
                tweet.text = $sce.trustAsHtml(tweet.text.replace(/(#[a-z0-9][a-z0-9\-_]*)/g,
                    '<span class="tag tagLink" ng-click>$1</span>'));
                // TWEET DATE
                var date = new Date(tweet.createdAt * 1000);
                tweet.date = date.toDateString() + " | " + date.getHours() + ":" + date.getMinutes();
            }
        });
        return tweets;
    };
    $rootScope.extractHashtags = function (tweets) {
        var hashtags = [];
        angular.forEach(tweets, function (tweet) {
            var temp = tweet.text.match(/(#[a-z0-9][a-z0-9\-_]*)/ig);
            angular.forEach(temp, function (hashtag) {
                if (hashtags.indexOf(hashtag) < 0) {
                    hashtags.push(hashtag)
                }
            })
        });
        console.log(hashtags);
        return hashtags;
    };
    $rootScope.seeFollowings = function (username) {
        $http.post(UrlConstants.followings, {
            username: username
        }).success(function (response) {
            $uibModal.open({
                templateUrl: 'pages/includes/modals/flwPeople.html',
                controller: function ($uibModalInstance) {
                    var mc = this;
                    mc.data = response;
                    mc.title = "Followings List";
                    mc.cancel = function () {
                        $uibModalInstance.dismiss();
                    }

                },
                size: 'md',
                controllerAs: 'mc'
            })
        })
    };
    $rootScope.seeFollowers = function (username) {
        $http.post(UrlConstants.followers, {
            username: username
        }).success(function (response) {
            $uibModal.open({
                templateUrl: 'pages/includes/modals/flwPeople.html',
                controller: function ($uibModalInstance) {
                    var mc = this;
                    mc.data = response;
                    mc.title = "Followers List";
                    mc.cancel = function () {
                        $uibModalInstance.dismiss();
                    }
                },
                size: 'md',
                controllerAs: 'mc'
            })
        })
    };
    $rootScope.logout = function () {
        $cookies.remove("token");
        $http.defaults.headers.common['Authorization'] = "";
        $state.go("home", {logout: true});
        $rootScope.loggedIn = false;
        Notify.success("Logged Out!", "You Logged Out Successfully!")
    };
    init();
});

