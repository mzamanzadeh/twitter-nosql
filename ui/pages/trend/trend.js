function trendCtrlFunction($rootScope, $scope, $http, UrlConstants) {
    var vm = this;
    vm.trends = [];

    function init() {
        $http.get(UrlConstants.trends).success(function (response) {
            angular.forEach(response, function (trend) {
                var j = {
                    name: trend[0],
                    count: trend[1]
            }
                vm.trends.push(j);
            })
        })
    }

    init();
}

angular.module("app").controller("trendsCtrl", trendCtrlFunction);