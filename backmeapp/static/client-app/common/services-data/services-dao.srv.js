(function(){
    angular
        .module('backMeAppModule')
        .factory('servicesDao.srv', factory);

    factory.$inject = [
        "$http",
        "$q"
    ]

    function factory($http, $q){

        return {
            getServicesData: function() {

                var deferred = $q.defer();

                $http.get("/services/services-data/").then(
                    function onSuccess(response) {
                        deferred.resolve(response.data);
                    },

                    function onFailure(response) {
                        console.error("Failed to get services data");
                        deferred.resolve({});
                    }
                );

                return deferred.promise;
            }
        }
    }

})();