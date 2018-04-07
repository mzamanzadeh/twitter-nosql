function usersCtrlFunction($rootScope, $stateParams, $http, UrlConstants) {
    var vm = this;
    vm.query = $stateParams.query;
    vm.userMode = true;

    function init() {
        $http.post(UrlConstants.searchUsers, {
            query: vm.query
        }).success(function (response) {
            vm.users = response;
        })
    }

    init();
}

angular.module("app").controller("usersCtrl", usersCtrlFunction);