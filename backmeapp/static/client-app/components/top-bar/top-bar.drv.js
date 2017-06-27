(function () {

    angular
        .module('backMeAppModule')
        .directive('topBar', topBarDirective);

    function topBarDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/components/top-bar/top-bar.tpl.html',
            controller: 'topBar.ctrl'
        }
    }

})();