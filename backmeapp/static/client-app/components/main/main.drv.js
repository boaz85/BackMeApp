(function () {

    angular
        .module('backMeAppModule')
        .directive('main', mainDirective);

    function mainDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/components/main/main.tpl.html',
            controller: 'main.ctrl'
        }
    }

})();