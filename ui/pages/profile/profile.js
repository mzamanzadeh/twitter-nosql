function profileCtrlFunction($stateParams, $http, UrlConstants, $rootScope) {
    var vm = this;
    vm.data = {};
    vm.username = $stateParams.username;

    function init() {
        $rootScope.getUserInfo().success(function () {
            $http.post(UrlConstants.profile, {
                username: vm.username
            }).success(function (response) {
                vm.data = response;
                vm.data.user = $rootScope.myData;
                vm.data.username = $rootScope.myData.username;
                vm.data.hashtags = $rootScope.extractHashtags(response.tweets);
                vm.data.tweets = $rootScope.processTweets(response.tweets);
                vm.data.info.tweetsCount = vm.data.tweets.length;
                vm.data.info.retweetsCount = $rootScope.countRetweets(response.tweets);
            })
        })
    }

    init();
}

angular.module("app").controller("profileCtrl", profileCtrlFunction);