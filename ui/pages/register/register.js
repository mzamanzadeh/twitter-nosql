function registerCtrlFunction($state, Notify, $http, UrlConstants) {
    var vm = this;
    vm.formData = {};
    vm.register = function () {
        $http.post(UrlConstants.register, vm.formData).success(function (response) {
            Notify.success("Register Successful!", "Please Login With Your Entered Credentials");
            $state.go("login");
        }).error(function () {
            Notify.error("Error", "Couldn't Register");
        })
    }
}

angular.module("app").controller("registerCtrl", registerCtrlFunction);