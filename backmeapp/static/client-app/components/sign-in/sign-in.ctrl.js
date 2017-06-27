(function () {

    angular
        .module('backMeAppModule')
        .controller('signIn.ctrl', signInCtrl);

    signInCtrl.$inject = [
        "signIn.srv",
        "userData.srv",
        "$location"
    ];

    function signInCtrl(signInService, userDataService, $location) {
        var vm = this;

        function onGoogleSignInSuccess(idToken, accessToken) {

            signInService.completeGoogleSignIn(idToken, accessToken).then(
                function() {return userDataService.getUserData(true)}).then(
                    function redirectToMainPage() {
                        $location.path("/");
                    }
                );
        }

        signInService.setGoogleSignInButton("backmeapp-googlesignin", onGoogleSignInSuccess);
    }

})();