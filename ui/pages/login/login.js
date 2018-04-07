function loginCtrlFunction($rootScope, UrlConstants, $http, Notify, $cookies, $state) {
    var vm = this;
    vm.formData = {};
    vm.login = function () {
        $http.post(UrlConstants.login, vm.formData).success(function (response) {
            Notify.success("Success", "Login Was Successful");
            $http.defaults.headers.common['Authorization'] = response.token;
            $cookies.put("token", response.token);
            $rootScope.loggedIn = true;
            $state.go("home");
            $http.get(UrlConstants.userInfo).success(function (response) {
                $rootScope.myData = response;
            })
        }).error(function () {
            Notify.error("Error", "Couldn't Login");
            $rootScope.loggedIn = false;
        })
    };
}

angular.module("app").controller("loginCtrl", loginCtrlFunction);