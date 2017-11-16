var app = angular.module('tiresApp', []).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});
app.filter('titlecase', function() {
    return function (input) {
        var smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;

        input = input.toLowerCase();
        if(input === undefined){ return null; }
        return input.replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g, function(match, index, title) {
            if (index > 0 && index + match.length !== title.length &&
                match.search(smallWords) > -1 && title.charAt(index - 2) !== ":" &&
                (title.charAt(index + match.length) !== '-' || title.charAt(index - 1) === '-') &&
                title.charAt(index - 1).search(/[^\s-]/) < 0) {
                return match.toLowerCase();
            }

            if (match.substr(1).search(/[A-Z]|\../) > -1) {
                return match;
            }

            return match.charAt(0).toUpperCase() + match.substr(1);
        });
    }
});
app.controller('tireListCtrl', function($scope, $http, $sce) {
    $scope.quantity = 0;
    $scope.currentPage = 1;
    $scope.paginate = function (page) {
        page = page || 1;
        $http({
            url: "/",
            method: "POST",
            data: {action:'paginate', page:page}
        }).then(function(response) {
            $scope.tires = JSON.parse(response.data.tires);
            $scope.quantity = page === 1 ? response.data.quantity : $scope.quantity;
            $scope.currentPage = page;
        }, function(response) {
            $(".alert.alert-danger").show();
        });
        window.setTimeout(function() {$(".alert").hide();}, 5000);
    };
    $scope.tires = $scope.paginate();
    $scope.deleteTire = function(pk) {
        $http({
            url: "/",
            method: "POST",
            data: {action:'delete', pk:pk}
        }).then(function(response) {
            var index;
            $scope.tires.forEach(function(value) {
                if (value.pk === pk) {
                    index = $scope.tires.indexOf(value);
                }
            });
            $scope.tires.splice(index, 1);
            $scope.quantity--;
            $(".alert.alert-success").show();
            $scope.tires.push(JSON.parse(response.data.tire)[0]);
        }, function(response) {
            $(".alert.alert-danger").show();
        });
        window.setTimeout(function() {$(".alert").hide();}, 5000);
    };
    $scope.deleteAll = function() {
        $http({
            url: "/",
            method: "POST",
            data: {action:'delete_all'}
        }).then(function(response) {
            $scope.quantity = 0;
            $scope.tires = [];
            $(".alert.alert-success").show();
        }, function(response) {
            $(".alert.alert-danger").show();
        });
        window.setTimeout(function() {$(".alert").hide();}, 5000);
    };
    $scope.add_or_edit_window = function(pk) {
        var data = pk ? {action:'add_or_edit_window', pk:pk} : {action:'add_or_edit_window'};
        $http({
            url: "/",
            method: "POST",
            data: data
        }).then(function(response) {
            $scope.window = $sce.trustAsHtml(response.data);
        }, function(response) {
            $(".alert.alert-danger").show();
        });
        window.setTimeout(function() {$(".alert").hide();}, 5000);
    };
});
