(function(){
    angular
        .module('backMeAppModule')
        .factory('signIn.srv', factory);

    factory.$inject = [
        "Initializer",
        "$http",
        "servicesData.srv",
        "userData.srv",
        "$q"
    ]

    function factory(Initializer, $http, servicesDataService, userDataService, $q){

        var GoogleSignInitialized = false;

        function initGoogleSignIn() {

            var deferred = $q.defer();

            if (GoogleSignInitialized) {
                deferred.resolve();
            }

            Initializer.signInInitialized.then(

                function() {

                    servicesDataService.getServiceData("google-signin").then(

                        function(googleSignInService) {
                            gapi.load('auth2', function () {

                                var initData = {client_id: googleSignInService.key,
                                                 scope: googleSignInService.scope.join(" ")};

                                gapi.auth2.init(initData).then(

                                     function() {
                                        GoogleSignInitialized = true;
                                        deferred.resolve();
                                     });
                            });
                        });
                });

            return deferred.promise;
        };

        return {

            setGoogleSignInButton: function(signInElementId, onSignInSuccess, onSignInFailures) {

                initGoogleSignIn().then(

                    function() {

                        function onSuccess(googleUser) {

                            if (onSignInSuccess) {

                                var idtoken = googleUser.getAuthResponse().id_token;
                                var access_token = googleUser.getAuthResponse().access_token;
                                onSignInSuccess(idtoken, access_token);
                            }
                        };

                        function loginFail(x) {

                            console.log("Google sign in failed");

                            if (onSignInFailures) {
                                onSignInFailures();
                            }
                        }

                        var renderData = {
                            'width': 300,
                            'height': 50,
                            'longtitle': true,
                            'theme': 'dark',
                            'onsuccess': onSuccess,
                            'onfailure': loginFail
                        };

                        gapi.signin2.render(signInElementId, renderData);
                });
            },

            completeGoogleSignIn: function(idToken, accessToken) {

                return servicesDataService.getServiceData("google-signin").then(function(googleSignInService) {

                    return $http({
                            method: 'POST',
                            url: googleSignInService.auth_complete,
                            data: $.param({idtoken: idToken, access_token: accessToken}),
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                        });
                });
            },

            backMeAppSignOut: function() {
                return $http.get('/users/sign-out/');
            },

            googleSignOut: function() {

                return initGoogleSignIn().then(function(){
                    var auth2 = gapi.auth2.getAuthInstance();
                    auth2.signOut();
                });
            },

            fullLogOut: function() {
                return this.backMeAppSignOut().then(this.googleSignOut).then(

                    function() {
                        userDataService.clearUserData();
                    });
            }
        }
    }

})();