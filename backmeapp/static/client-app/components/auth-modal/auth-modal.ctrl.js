//(function () {
//
//    angular
//        .module('backMeAppModule')
//        .controller('authModal.ctrl', authModal);
//
//    authModal.$inject = [
//        "$modalInstance",
//        "authSrc",
//        "$sce"
//    ];
//
//    function authModal($modalInstance, authSrc, $sce) {
//        var vm = this;
//
//        vm.authSrc = $sce.trustAsResourceUrl(authSrc);
//
//        vm.dismiss = $modalInstance.dismiss;
//
//    }
//
//})();