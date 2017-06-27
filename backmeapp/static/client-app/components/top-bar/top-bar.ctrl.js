(function () {

    angular
        .module('backMeAppModule')
        .controller('topBar.ctrl', topBarCtrl);

    topBarCtrl.$inject = [
        "$location",
        "userData.srv",
        "signIn.srv"
    ];

    function topBarCtrl($location, userDataService, signInService) {
        var vm = this;

        userDataService.getUserData().then(
            function(userData) {
                vm.userData = userData;
            }
        )

        vm.itemClicked = itemClicked;

        vm.goHome = goHome;

        vm.activePath = $location.path();

        vm.accountItems = [
                            {text: 'Join', path: '/join', hideFromLoggedIn: true},
                            {text: 'Sign In', path: '/sign-in', hideFromLoggedIn: true},
                            {text: 'Sign out', path: '/sign-out', action: signOut, hideFromLoggedOut: true}
                          ];

        vm.backupItems = [
                            {text: 'New Backup', path: '/new-backup', hideFromLoggedOut: true},
                            {text: 'My Backups', path: '/my-backups', hideFromLoggedOut: true}
                          ];

        function itemClicked(item) {

            vm.activePath = item.path;

            if (item.hasOwnProperty('action')) {
                item.action();

            } else {
                $location.path(item.path);
            }
        }

        function goHome() {
            vm.activePath = "/";
            $location.path("/");
        }

        function signOut() {
            signInService.fullLogOut().then(
                function() {
                    $location.path("/");
                }
            )
        }
    }
})();