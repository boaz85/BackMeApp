(function () {

    angular
        .module('backMeAppModule')
        .directive('signIn', signInDirective);

    function signInDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/components/sign-in/sign-in.tpl.html',
            controller: 'signIn.ctrl'
        }
    }

})();