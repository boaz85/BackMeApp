angular.module('backMeAppModule')
    .factory('Initializer', function($window, $q){

        var signInDefer = $q.defer();

        var asyncUrl = 'https://apis.google.com/js/platform.js?onload=';

        var asyncLoad = function(asyncUrl, callbackName) {
          var script = document.createElement('script');
          //script.type = 'text/javascript';
          script.src = asyncUrl + callbackName;
          document.body.appendChild(script);
        };

        $window.googleSignInInitialized = signInDefer.resolve;

        asyncLoad(asyncUrl, 'googleSignInInitialized');

        return {

            signInInitialized : signInDefer.promise
        };
    })