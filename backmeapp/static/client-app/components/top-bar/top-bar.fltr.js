(function () {

    angular
        .module('backMeAppModule')
        .filter('topBarFilter', topBarFilter);

    function topBarFilter () {
        return function (items, isLoggedIn) {
            if (!items) {
                return [];
            }

            var filtered = [];

            for (var i=0; i<items.length; ++i) {
                var item = items[i];

                if (isLoggedIn && !item.hideFromLoggedIn) {
                    filtered.push(item);

                } else if (!isLoggedIn && !item.hideFromLoggedOut) {
                    filtered.push(item);
                }
            }

            return filtered;
        };
    }

})();