/**
 * Fourletterphat service.
 * Handle fourletterphat application requests.
 * Service is the place to store your application content (it is a singleton) and
 * to provide your application functions.
 */
angular
.module('Cleep')
.service('fourletterdisplayService', ['$rootScope', 'rpcService',
function($rootScope, rpcService) {
    var self = this;

    /**
     * Set brightness
     */
    self.setBrightness = function(brightness) {
        return rpcService.sendCommand('set_brightness', 'fourletterdisplay', {
            'brightness': brightness
        });
    };

    /**
     * Set night mode brightness
     */
    self.setNightModeBrightness = function(brightness) {
        return rpcService.sendCommand('set_night_mode_brightness', 'fourletterdisplay', {
            'brightness': brightness
        });
    };

    /**
     * Display message
     */
    self.displayMessage = function(message) {
        return rpcService.sendCommand('display_message', 'fourletterdisplay', {
            'message': message
        });
    };

    /**
     * Set dots
     */
    self.setDots = function(mostLeft, middleLeft, middleRight, mostRight) {
        return rpcService.sendCommand('set_dots', 'fourletterdisplay', {
            'most_left': mostLeft,
            'middle_left': middleLeft,
            'middle_right': middleRight,
            'most_right': mostRight,
        });
    };

    /**
     * Enable night mode
     */
    self.enableNightMode = function(enable) {
        return rpcService.sendCommand('enable_night_mode', 'fourletterdisplay', {
            'enable': enable
        });
    };

    /**
     * Clear display
     */
    self.clear = function(enable) {
        return rpcService.sendCommand('clear', 'fourletterdisplay');
    };

}]);

