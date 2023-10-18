/**
 * Fourletterdisplay config component
 * Handle fourletterdisplay application configuration
 */
angular
.module('Cleep')
.directive('fourletterdisplayConfigComponent', ['$rootScope', 'cleepService', 'fourletterdisplayService',
function($rootScope, cleepService, fourletterdisplayService) {

    var fourletterdisplayConfigController = function() {
        var self = this;
        self.config = {};
        self.message = '';
        self.dotsOptions = [
            { label: 'left dot', value: 0 },
            { label: 'middle-left dot', value: 1 },
            { label: 'middle-right dot', value: 2 },
            { label: 'right dot', value: 3 },
        ];
        self.selectedDots = [];

        self.displayMessage = function() {
            fourletterdisplayService.displayMessage(self.message);
            self.message = '';
        };

        self.setDots = function(value) {
            const dots = new Array(4).fill(false);
            value.forEach((dot) => dots[dot] = true);
            fourletterdisplayService.setDots(dots[0], dots[1], dots[2], dots[3]);
        };

        self.enableNightMode = function(value) {
            fourletterdisplayService.enableNightMode(value)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay')
                });
        };

        self.setBrightness = function(value) {
            fourletterdisplayService.setBrightness(value)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay')
                });
        };

        self.setNightModeBrightness = function(value) {
            fourletterdisplayService.setNightModeBrightness(value)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay');
                });
        };

        self.clearDisplay = function() {
            fourletterdisplayService.clear();
        };

        self.$onInit = function() {
            cleepService.getModuleConfig('fourletterdisplay');
        };

        /**
         * Keep app configuration in sync
         */
        $rootScope.$watch(function() {
            return cleepService.modules['fourletterdisplay'].config;
        }, function(newVal, oldVal) {
            if(newVal && Object.keys(newVal).length) {
                Object.assign(self.config, newVal);
            }
        });
    };

    return {
        templateUrl: 'fourletterdisplay.config.html',
        replace: true,
        scope: true,
        controller: fourletterdisplayConfigController,
        controllerAs: '$ctrl',
    };
}]);

