(function () {

    angular
        .module('backMeAppModule')
        .controller('emailGroupersSelect.ctrl', emailGroupersSelectCtrl);

    emailGroupersSelectCtrl.$inject = [

    ];

    function emailGroupersSelectCtrl() {
        var vm = this;
        var multiselect = $("#multiselect");
        multiselect.multiselect();
    }

})();