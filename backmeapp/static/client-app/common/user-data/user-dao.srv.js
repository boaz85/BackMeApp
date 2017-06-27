(function(){
    angular
        .module('backMeAppModule')
        .factory('userDao.srv', factory);

    factory.$inject = [
        "$http"
    ]

    function factory($http){

        return {

            getUserData: function() {
                return $http.get('/users/user-data/');
            },

            isAuthorized: function(service) {
                return $http.get('/users/is-authorized?service=' + service);
            },

            getEmailGroupers: function(service) {
                return $http.get('/services/email-groupers?service=' + service).then(
                    function(response) {
                        return response.data;
                    });
            }
        }
    }

})();