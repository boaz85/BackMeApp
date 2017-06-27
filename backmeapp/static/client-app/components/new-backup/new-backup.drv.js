(function () {

    angular
        .module('backMeAppModule')
        .directive('newBackup', newBackupDirective);

    function newBackupDirective() {
        return {
            controllerAs: 'vm',
            restrict: 'E',
            templateUrl: '/static/client-app/components/new-backup/new-backup.tpl.html',
            controller: 'newBackup.ctrl'
        }
    }

})();