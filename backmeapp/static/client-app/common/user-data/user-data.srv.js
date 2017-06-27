(function(){
    angular
        .module('backMeAppModule')
        .factory('userData.srv', factory);

    factory.$inject = [
        "$q",
        "userDao.srv",
    ]

    function factory($q, userDaoService){

        var deferred = null;

        var userData = {isLoggedIn: false};

        return {

            getUserData: function(forceReload) {

                if (deferred && !forceReload) {
                    return deferred.promise;
                }

                if (!deferred) {
                    deferred = $q.defer();
                }

                userDaoService.getUserData().then(
                    function onSuccess(response) {

                        //Keep the same reference
                        for (var p in response.data) {
                            userData[p] = response.data[p];
                        }

                        deferred.resolve(userData);
                    },

                    function onFailure(response) {
                        console.error(response.status.toString());
                        deferred.reject("Failed to fetch userData from server");
                    }
                );

                return deferred.promise;
            },

            clearUserData() {
                for (var p in userData) {
                    delete userData[p];
                }

                userData.isLoggedIn = false;
            },

            getUserEmailGroupers(serviceSlug) {
                return userDaoService.emailGroups(serviceSlug);
            }
        }
    }

})();