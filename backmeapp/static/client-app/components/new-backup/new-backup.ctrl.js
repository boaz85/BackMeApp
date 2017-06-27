(function () {

    angular
        .module('backMeAppModule')
        .controller('newBackup.ctrl', newBackup);

    newBackup.$inject = [
        "$window",
        "$scope",
        "servicesData.srv",
        "userDao.srv",
        "$q"
    ];

    function newBackup($window, $scope, servicesDataService, userDaoService, $q) {
        var vm = this;

        servicesDataService.getEmailServices().then(
            function onSuccess(emailServices) {
                vm.emailServices = emailServices;
                vm.selectedEmailService = emailServices[0];
            }
        );

        servicesDataService.getStorageServices().then(

            function onSuccess(storageServices) {
                vm.storageServices = storageServices;
                vm.selectedStorageService = storageServices[0];
            }
        );

        vm.emailAuthRequired = false;
        vm.storageAuthRequired = false;

        vm.emailAuthSucceed = false;
        vm.storageAuthSucceed = false;

        vm.startEmailAuthentication = startEmailAuthentication;
        vm.startStorageAuthentication = startStorageAuthentication;

        vm.selectEmailService = selectEmailService;
        vm.selectStorageService = selectStorageService;

        function selectEmailService(service) {
            vm.selectedEmailService = service;

            userDaoService.isAuthorized(service.slug).then(

                function(response) {

                    if (response.data == "True") {
                        vm.emailAuthRequired = false;
                        userDaoService.getEmailGroupers(vm.selectedEmailService.slug).then(
                            function showEmailGroupers(groupersData) {
                                vm.allEmailGroupers = groupersData.all_groupers;
                                vm.selectedEmailGroupers = groupersData.selected_groupers;
                            }
                        );

                    } else {
                        vm.emailAuthSucceed = false;
                        vm.emailAuthRequired = true;
                    }
                }
            );
        }

        function selectStorageService(service) {
            vm.selectedStorageService = service;

            userDaoService.isAuthorized(service.slug).then(

                function(response) {
                    if (response.data == "True") {
                        vm.storageAuthRequired = false;

                    } else {
                        vm.storageAuthSucceed = false;
                        vm.storageAuthRequired = true;
                    }
                }
            );
        }

        function startEmailAuthentication() {

            if (vm.selectedEmailService == null) {
                vm.noEmailServiceChosen = true;
                return;

            } else {
                vm.noEmailServiceChosen = false;
            }

            startAuth(vm.selectedEmailService.auth_url).then(
                function() {
                    vm.emailAuthSucceed = true;
                    vm.emailAuthRequired = false;

                    userDaoService.getEmailGroupers(vm.selectedEmailService.slug).then(
                        function showEmailGroupers(groupersData) {
                            vm.allEmailGroupers = groupersData.all_groupers;
                            vm.selectedEmailGroupers = groupersData.selected_groupers;
                        }
                    );
                }
            );
        }

        function startStorageAuthentication() {

            if (vm.selectedStorageService == null) {
                vm.noStorageServiceChosen = true;

            } else {
                vm.noStorageServiceChosen = false;
            }

            startAuth(vm.selectedStorageService.auth_url).then(
                function() {
                    vm.storageAuthSucceed = true;
                    vm.storageAuthRequired = false;
                }
            );
        }

        function startAuth(url) {

            var deferred = $q.defer();

            var authWindow;

            $window.onAuthFinish = function() {

                $scope.$apply(function () {
                    deferred.resolve();
                });

                authWindow.close();
            }

            authWindow = $window.open(url, 'BackMeApp', "width=600,height=450");

            return deferred.promise;
        }
    }

})();