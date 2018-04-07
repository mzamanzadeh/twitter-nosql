angular.module('app').service('Notify', ['toastr', notificationServiceFunction]);
function notificationServiceFunction(toastr) {
    this.clear = function () {
        toastr.clear();
    };
    this.info = function (title, text) {
        toastr.info(text, title);
    };
    this.warning = function (title, text) {
        toastr.warning(text, title);
    };
    this.success = function (title, text) {
        toastr.success(text, title);
    };
    this.error = function (title, text) {
        toastr.error(text, title);
    };
}