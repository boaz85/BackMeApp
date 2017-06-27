(function () {

    angular
        .module('backMeAppModule')
        .directive('emailGroupersSelect', emailGroupersSelectDirective);

    function emailGroupersSelectDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/common/email-groupers-select/email-groupers-select.tpl.html',
            controller: 'emailGroupersSelect.ctrl',
            scope: {allGroupers: '=',
                    selectedGroupers: '='},
            link: function (scope, element, attrs, emailGroupersSelectController) {
                emailGroupersSelectController.allGroupers = scope.allGroupers;
                emailGroupersSelectController.selectedGroupers = scope.selectedGroupers;
                emailGroupersSelectController.id = attrs.id;
            }
        }
    }

})();