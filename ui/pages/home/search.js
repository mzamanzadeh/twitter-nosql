function searchCtrlFunction($rootScope, $scope, $stateParams){
    var vm = this;
    vm.query = $stateParams.query;
    vm.searchMode = true;
    console.log(vm.query);
}
angular.module("app").controller("searchCtrl", searchCtrlFunction);