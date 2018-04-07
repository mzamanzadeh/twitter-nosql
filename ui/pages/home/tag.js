function tagCtrlFunction($rootScope, $http, $stateParams, UrlConstants) {
    var vm = this;
    vm.tag = $stateParams.tagName;
    vm.tagMode = true;

    function init() {
        $http.post(UrlConstants.searchHashtags, {
            query: vm.tag
        }).success(function (response) {
            vm.tweets = $rootScope.processTweets(response);
        })
    }

    init();
}

angular.module("app").controller("tagCtrl", tagCtrlFunction);