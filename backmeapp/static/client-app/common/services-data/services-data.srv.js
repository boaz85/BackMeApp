(function(){
    angular
        .module('backMeAppModule')
        .factory('servicesData.srv', factory);

    factory.$inject = [
        "$q",
        "servicesDao.srv"
    ]

    function factory($q, servicesDaoService){

        var deferred = null;

        var servicesData = null;
        var emailServices = [];
        var signInServices = [];
        var storageServices = [];
        var serviceBySlug = {};

        function processServicesData(servicesData) {

            for (var i = 0; i < servicesData.length; ++i) {

                if (servicesData[i].service_type == ServiceEnum.EMAIL) {
                    emailServices.push(servicesData[i]);
                } else if (servicesData[i].service_type == ServiceEnum.SIGNIN) {
                    signInServices.push(servicesData[i]);
                } else if (servicesData[i].service_type == ServiceEnum.STORAGE) {
                    storageServices.push(servicesData[i]);
                }

                serviceBySlug[servicesData[i].slug] = servicesData[i];
            }
        }

        return {

            getEmailServices: function() {
                var deferred = $q.defer();
                this.getServicesData().then(function(){deferred.resolve(emailServices)});
                return deferred.promise;
            },

            getSignInServices: function() {
                var deferred = $q.defer();
                this.getServicesData().then(function(){deferred.resolve(signInServices)});
                return deferred.promise;
            },

            getStorageServices: function() {
                var deferred = $q.defer();
                this.getServicesData().then(function(){deferred.resolve(storageServices)});
                return deferred.promise;
            },

            getServiceData: function(slug) {
                var deferred = $q.defer();
                this.getServicesData().then(function(){deferred.resolve(serviceBySlug[slug])});
                return deferred.promise;
            },

            getServicesData: function() {

                if (deferred) {
                    return deferred.promise;
                }

                deferred = $q.defer();

                servicesDaoService.getServicesData().then(
                    function(servicesData) {
                        servicesData = servicesData;
                        processServicesData(servicesData);
                        deferred.resolve(servicesData);
                    }
                );

                return deferred.promise;
            }
        }
    }

})();