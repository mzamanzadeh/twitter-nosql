function logCtrlFunction($rootScope, $scope, $http, UrlConstants) {
    var vm = this;
    vm.logs = [];

    function init() {
        $http.get(UrlConstants.logs).success(function (response) {
            vm.logs = response;
        })
    }

    init();
}

angular.module("app").controller("logsCtrl", logCtrlFunction);