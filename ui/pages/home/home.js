function homeCtrlFunction($rootScope, $http, UrlConstants, $stateParams) {
    var vm = this;
    vm.homeMode = true;

    function init() {
        if (!$stateParams.logout)
            $http.get(UrlConstants.timeline).success(function (response) {
                vm.tweets = $rootScope.processTweets(response);
            }).error(function (response) {
            })
    }

    init();
}

angular.module("app").controller("homeCtrl", homeCtrlFunction);