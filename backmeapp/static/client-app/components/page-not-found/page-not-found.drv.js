(function () {

    angular
        .module('backMeAppModule')
        .directive('pageNotFound', pageNotFoundDirective);

    function pageNotFoundDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/components/page-not-found/page-not-found.tpl.html',
            controller: 'pageNotFound.ctrl'
        }
    }

})();