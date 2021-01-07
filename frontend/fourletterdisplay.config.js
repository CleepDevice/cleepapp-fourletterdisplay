/**
 * Fourletterdisplay config component
 * Handle fourletterdisplay application configuration
 * If your application doesn't need configuration page, delete this file and its references into desc.json
 */
angular
.module('Cleep')
.directive('fourletterdisplayConfigComponent', ['$rootScope', 'cleepService', 'fourletterdisplayService',
function($rootScope, cleepService, fourletterdisplayService) {

    var fourletterdisplayConfigController = function() {
        var self = this;
        self.config = {};
        self.message = '';
        self.dots = [false, false, false, false];

        /**
         * Display message
         */
        self.displayMessage = function() {
            fourletterdisplayService.displayMessage(self.message);
        };

        /**
         * Set dots
         */
        self.setDots = function() {
            fourletterdisplayService.setDots(self.dots[0], self.dots[1], self.dots[2], self.dots[3]);
        };

        /**
         * Enable night mode
         */
        self.enableNightMode = function() {
            fourletterdisplayService.enableNightMode(self.config.nightmode)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay')
                });
        };

        /**
         * Set default brightness
         */
        self.setBrightness = function() {
            fourletterdisplayService.setBrightness(self.config.brightness)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay')
                });
        };

        /**
         * Set night mode brightness
         */
        self.setNightModeBrightness = function() {
            fourletterdisplayService.setNightModeBrightness(self.config.nightbrightness)
                .then(function(resp) {
                    cleepService.reloadModuleConfig('fourletterdisplay');
                });
        };

        /**
         * Clear display
         */
        self.clear = function() {
            fourletterdisplayService.clear();
        };

        /**
         * Init component
         */
        self.$onInit = function() {
            // get module config
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
        controllerAs: 'fourletterdisplayCtl',
    };
}]);

