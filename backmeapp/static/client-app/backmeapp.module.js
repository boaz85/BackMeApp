
var backMeAppModule = angular.module('backMeAppModule', ['ngRoute', 'ui.bootstrap']);

backMeAppModule.config([
    '$routeProvider', '$httpProvider', '$locationProvider',
    function ($routeProvider, $httpProvider, $locationProvider) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        var html5Mode = !!(window.history && history.pushState);
        $locationProvider.html5Mode(html5Mode ? {enabled: true, requireBase: false} : false);
        setRoutes($routeProvider);

    }
]);

function setRoutes($routeProvider) {

    $routeProvider.when("/",        {template: "<main></main>"});
    $routeProvider.when("/404",     {template: "<page-not-found></page-not-found>"});

    $routeProvider.when("/sign-in", {template: "<sign-in></sign-in>"});
    $routeProvider.when("/new-backup", {template: "<new-backup></new-backup>"});

    $routeProvider.otherwise({redirectTo: "/404"})
}