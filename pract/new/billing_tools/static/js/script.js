var app = angular.module('billingTools', ["Chart.js", 'easypiechart', 'ui.bootstrap', 'ngRoute', 'ngAnimate', 'ngMessages', 'ngSanitize', 'ngCookies',
    'ngToast', 'ngCookies']);


app.config(['ngToastProvider', function (ngToastProvider) {
    ngToastProvider.configure({
        horizontalPosition: 'center',
        maxNumber: 1
    });
}]);

app.controller('hlrCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "$filter", "$http", "$interval", '$modal',
    function ($scope, $window, $location, $cookies, $timeout, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.servicePending = false;
        $scope.all_topics = [];
        $scope.inputParam = "";
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });
        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

        $scope.get_hlr_data = function () {
            var warehouse_post_data = {};

            $scope.servicePending = false;
            warehouse_post_data = {
                topic: "subscription_conversion",
                query: $scope.selectedTopic.query,
                ISDN: $scope.selectedTopic.inputParam
            }
            var url = $location.protocol() + "://" + $location.host() + ":9001/run_cmd_cmds";
            $http({
                url: url,
                method: "POST",
                data: warehouse_post_data
            }).then(function (response) {
                $scope.servicePending = true;
                $scope.warehouseData = response.data;
            }, function (response) {

                $scope.servicePending = true;
            });
        }
    }]);


app.controller('wareHouseCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "$filter", "$http", "$interval", '$modal',
    function ($scope, $window, $location, $cookies, $timeout, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.servicePending = false;
        $scope.all_topics = [];
        $scope.inputParam = "";
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });
        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

        $scope.get_ware_house_data = function () {
            var warehouse_post_data = {};
            if ($scope.selectedTopic.query == "check_lot" || $scope.selectedTopic.query == "check_device_inventroy") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    lot_id: $scope.selectedTopic.inputParam
                }
            }
            if ($scope.selectedTopic.query == "check_bin") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    bin_id: $scope.selectedTopic.inputParam
                }
            }
            if ($scope.selectedTopic.query == "check_device") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    serial_number: $scope.selectedTopic.inputParam
                }
            }
            if ($scope.selectedTopic.query == "trace_reseller_request") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    iccid: "ServiceBundled-" + $scope.selectedTopic.inputParam
                }
            }
            if ($scope.selectedTopic.query == "check_product_reserve_state" || $scope.selectedTopic.query == "check_reseller_request") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    request_id: $scope.selectedTopic.inputParam
                }
            }
            if ($scope.selectedTopic.query == "check_stock_assignment") {
                warehouse_post_data = {
                    topic: "warehouse",
                    query: $scope.selectedTopic.query,
                    serial_start: $scope.selectedTopic.inputParam,
                    serial_end: $scope.selectedTopic.inputParam
                }
            }
            $scope.servicePending = false;
            var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
            $http({
                url: url,
                method: "POST",
                data: warehouse_post_data
            }).then(function (response) {
                $scope.servicePending = true;
                $scope.warehouseData = response.data;
            }, function (response) {

                $scope.servicePending = true;
            });
        }
    }]);

app.controller('ussdCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "$filter", "$http", "$interval", '$modal',
    function ($scope, $window, $location, $cookies, $timeout, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.servicePending = false;
        $scope.all_topics = [];
        $scope.inputParam = "";
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });
        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

        $scope.get_ussd_data = function () {
            var ussd_data = {};
            if ($scope.selectedTopic.query == "check_ussd_code") {
                var ussd_data = {
                    topic: "ussd",
                    query: $scope.selectedTopic.query,
                    inputParam: {
                        ussd_code: $scope.selectedTopic[0].inputParam,
                        servedMSISDN: $scope.selectedTopic[1].inputParam

                    }
                }
            }
            $scope.servicePending = false;
            var url = $location.protocol() + "://" + $location.host() + ":9001/check_ussd_codes";
            $http({
                url: url,
                method: "POST",
                data: ussd_data
            }).then(function (response) {
                $scope.servicePending = true;
                $scope.ussd = response.data;
            }, function (response) {

                $scope.servicePending = true;
            });
        }
    }]);

app.controller("detailsModelCtrl", ['$scope', '$modalInstance', 'ngToast', 'userId', '$window', '$location',
    function ($scope, $modalInstance, ngToast, userId, $window, $location) {
        $scope.close_popup = function () {
            $modalInstance.close('working');
        };
        $scope.tableData = [];
        $scope.tableRowVet = userId.selectTr;
        $scope.tableHeadvet = userId.selectTh;
        angular.forEach($scope.tableHeadvet, function (value, index) {
            var details = {
                header: value,
                RowVet: $scope.tableRowVet[index]
            }
            $scope.tableData.push(details)
        })
    }]);

app.controller('helpDeskCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();

        $scope.servicePending = false;
        $scope.all_topics = [];
        $scope.inputParam = "";
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });

        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
        $scope.get_help_desk_data = function () {
            $scope.servicePending = false;
            var url = $location.protocol() + "://" + $location.host() + ":9001/";
            $http({
                url: url,
                method: "POST",
                data: { "topic": "helpdesk", "query": $scope.selectedTopic.query, "ticket_id": $scope.selectedTopic.inputParam }
            }).then(function (response) {
                $scope.servicePending = true;
                $scope.helpDeskData = response.data;
            }, function (response) {
                $scope.servicePending = true;
            });
        }
    }]);
app.controller('registrationCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();


        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });

        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
        $scope.nin = "";
        $scope.surName = "";

        $scope.givenNames = "";
        $scope.otherNames = "",
            $scope.dob = "",
            $scope.documentId = "";

        $scope.get_registration_data = function () {
            $scope.servicePending = false;

            if ($scope.selectedTopic.query == 'check_registration') {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "registration", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            else if ($scope.selectedTopic.query == 'nira_verification') {
                dob = $filter('date')($scope.dob, "dd/MM/YYYY");
                $scope.inputParam = {
                    "nin": $scope.nin,
                    "surName": $scope.surName,
                    "surName": $scope.surName,
                    "givenNames": $scope.givenNames,
                    "otherNames": $scope.otherNames,
                    "dob": $scope.dob,
                    "documentId": $scope.documentId
                }
                var url = $location.protocol() + "://" + $location.host() + ":9002/verify_nira_info";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "registration", "query": $scope.selectedTopic.query, "queries": $scope.selectedTopic, "inputParam": $scope.inputParam }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.niradetails = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            } else if ($scope.selectedTopic.query == 'refugee_validation') {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "registration", "query": $scope.selectedTopic, "user_name": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }
    }]);

app.controller('rechargeCancelCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();


        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true
        })
        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
        $scope.get_registration_data = function () {
            $scope.servicePending = false;
            var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
            $http({
                url: url,
                method: "POST",
                data: { "topic": "recharge_cancellation", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic.inputParam }
            }).then(function (response) {
                $scope.helpDeskData = response.data;
                $scope.servicePending = true;
            }, function (response) {

            });
        }
    }]);

app.controller('dataServiceCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });

        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

        $scope.get_registration_data = function () {

            if ($scope.selectedTopic.query == "check_rated_CDRS") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "data_service", "query": $scope.selectedTopic.query, "served_IMSI": $scope.selectedTopic[0].inputParam, "commit_date_start": $scope.selectedTopic[1].inputParam, "commit_date_end": $scope.selectedTopic[2].inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            } else {
                $scope.servicePending = true;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "data_service", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }
    }]);

app.controller('VoiceServiceCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.all_topics = [];
        $scope.served_MSISDN = "";
        $scope.rec_limit = "";
        $scope.cur_date = "";
        $scope.called_number = "";
        $scope.servicePending = false;
        $scope.inputParam = "";
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });

        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

        $scope.get_registration_data = function () {
            if ($scope.selectedTopic.query == "suitable_onnet_subscriptions") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "cur_date": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10) }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = false;
                });
            }

            if ($scope.selectedTopic.query == "check_call_trace") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "called_number": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10) }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

            if ($scope.selectedTopic.query == "check_sms_trace") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "called_number": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10) }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            if ($scope.selectedTopic.query == "last_sms_usage") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "tariff_type": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10), "cur_date": $scope.selectedTopic[3].inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            if ($scope.selectedTopic.query == "offnet_international_subscriptions") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "ndc": $scope.selectedTopic[1].inputParam, "cur_date": $scope.selectedTopic[2].inputParam, "rec_limit": parseInt($scope.selectedTopic[3].inputParam, 10) }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            if ($scope.selectedTopic.query == "called_number_superonnet_check") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "called_number": $scope.selectedTopic[0].inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                }, function (response) {

                });
            }
            if ($scope.selectedTopic.query == "last_call_usage") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "tariff_type": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10), "cur_date": $scope.selectedTopic[3].inputParam }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            if ($scope.selectedTopic.query == "suitable_superonnet_subscriptions") {
                $scope.servicePending = false;
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "call_trace", "query": $scope.selectedTopic.query, "served_MSISDN": $scope.selectedTopic[0].inputParam, "cur_date": $scope.selectedTopic[1].inputParam, "rec_limit": parseInt($scope.selectedTopic[2].inputParam, 10) }
                }).then(function (response) {
                    $scope.servicePending = true;
                    $scope.helpDeskData = response.data;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }


    }]);

app.controller('eventCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();


        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });


        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
        $scope.get_registration_data = function () {
            var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
            if ($scope.selectedTopic.query == "check_events") {
                var start_date = $filter('date')($scope.start_date, "yyyy-MM-dd");

                var end_date = $filter('date')($scope.end_date, "yyyy-MM-dd");
                $scope.servicePending = false;
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "events", "query": $scope.selectedTopic.query, "event_desc": '%' + $scope.event_desc + '%', "start_date": start_date, "end_date": end_date }
                }).then(function (response) {
                    $scope.eventsData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            } else {
                var start_date = $filter('date')($scope.start_date, "yyyy-MM-dd");

                var end_date = $filter('date')($scope.end_date, "yyyy-MM-dd");
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "events", "query": $scope.selectedTopic.query, "error_desc": '%' + $scope.event_desc + '%', "start_date": start_date, "end_date": end_date }
                }).then(function (response) {
                    $scope.eventsData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                })
            }
        }
    }]);

app.controller('rechargeCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();


        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        })


        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
        $scope.get_registration_data = function () {
            $scope.servicePending = false;
            if ($scope.selectedTopic.query == "check_recharge_with_recharge_token") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "recharge_details", "query": $scope.selectedTopic.query, "bundle_record_token": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

            if ($scope.selectedTopic.query == "check_recharge_with_payment_id") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "recharge_details", "query": $scope.selectedTopic.query, "payment_id": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }
    }]);



app.controller('debugLogCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();

        $scope.all_topics = [];
        //$scope.selectedTopic.inputParam=[]
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.servicePending = true;
            $scope.all_topics = response.data;
        })

        $scope.input_params = [
            { value: "" }
        ];
        $scope.add_param = function () {
            $scope.input_params.push({ value: "" })
        };
        $scope.onclick_get_issues = function (value, index) {

        }

        $scope.get_registration_data = function () {
            $scope.servicePending = false;
            var url = $location.protocol() + "://" + $location.host() + ":9001/check_debug_logs";
            $http({
                url: url,
                method: "POST",
                data: { "topic": "cmd_interface", "query": $scope.selectedTopic.query, "filter": $scope.selectedTopic[0].inputParam }
            }).then(function (response) {
                $scope.helpDeskData = response.data;
                $scope.servicePending = true;
            }, function (response) {
                $scope.servicePending = true;
            });
        }

    }]);

app.controller('logCheckCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();

        $scope.all_topics = [];
        //$scope.selectedTopic.inputParam=[]
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_log_topics";
        $http.get(url).then(function (response) {
            $scope.servicePending = true;
            $scope.all_topics = response.data;
        })

        $scope.input_params = [
            { value: "" }
        ];
        $scope.add_param = function () {
            $scope.input_params.push({ value: "" })
        };
        $scope.onclick_get_issues = function (value, index) {

        }

        $scope.get_registration_data = function () {
            var finalArray = []
            //finalArray = $scope.selectedInput.map(function (obj) {return obj.value;});
            var finalArray = []
            angular.forEach($scope.selectedTopic.inputParam, function (value, index) {
                finalArray.push(value)
            })

            var url = $location.protocol() + "://" + $location.host() + ":9001/check_logs";
            $http({
                url: url,
                method: "POST",
                data: { "topic": "log_check", 'sub_topic_issue': 'Email Not Reviced', "pattern": $scope.issueType, "query": $scope.selectedTopic.query, "input_params": finalArray }
            }).then(function (response) {
                $scope.eventsData = response.data.result;
            }, function (response) {

            });
        }

    }]);

app.controller('voucherCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();


        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        })


        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });

                    }
                }

            }, function () {

            });
        };
        $scope.get_registration_data = function () {
            $scope.servicePending = false;
            if ($scope.selectedTopic.query == "check_reseller_voucher_request_state") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "vouchers", "query": $scope.selectedTopic.query, "request_id": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

            if ($scope.selectedTopic.query == "check_voucher_batch_state") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "vouchers", "query": $scope.selectedTopic.query, "voucher_bach_id": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

            if ($scope.selectedTopic.query == "check_voucher_status_using_voucher_code") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "vouchers", "query": $scope.selectedTopic.query, "voucher_code": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

            if ($scope.selectedTopic.query == "check_voucher_status_using_bundle_token") {

                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "vouchers", "query": $scope.selectedTopic.query, "bundle_token": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.helpDeskData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }

        }
    }]);


app.controller('applictionCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });
        $scope.get_application_data = function () {
            $scope.servicePending = false;
            if ($scope.selectedTopic.query == "active_reseller_sessions") {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                var date = $filter('date')($scope.selectedTopic.inputParam, "yyyy-MM-dd");
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "application", "query": $scope.selectedTopic.query, "date": '%' + date + '%' }
                }).then(function (response) {
                    $scope.applicationData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });

            } else if ($scope.selectedTopic.query == "application") {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "application", "query": $scope.selectedTopic.query, "msisdn": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.applicationData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }

        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });

                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };
    }]);


app.controller('documentsCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });
        $scope.get_documents_data = function () {
            $scope.servicePending = false;
            if ($scope.selectedTopic.query == 'visa_update_failed') {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "document_issues", "query": $scope.selectedTopic.query, "user_name": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.applicationData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            else if ($scope.selectedTopic.query == 'visa_update_reseller_permissions') {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "document_issues", "query": $scope.selectedTopic.query, "reseller_name": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.applicationData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
            else if ($scope.selectedTopic.query == 'Check_missing_documents') {
                var url = $location.protocol() + "://" + $location.host() + ":9001/run_query";
                $http({
                    url: url,
                    method: "POST",
                    data: { "topic": "document_issues", "query": $scope.selectedTopic.query, "user_name": $scope.selectedTopic.inputParam }
                }).then(function (response) {
                    $scope.applicationData = response.data;
                    $scope.servicePending = true;
                }, function (response) {
                    $scope.servicePending = true;
                });
            }
        }
        $scope.detail_row = function (tableHead, tableRow) {
            var userModalInstance = $modal.open({
                templateUrl: '/static/js/details.html',
                controller: 'detailsModelCtrl',
                keyboard: true,
                resolve: {
                    userId: function () {
                        return {
                            'selectTh': tableHead,
                            'selectTr': tableRow
                        }
                    }
                },
                size: 'lg'
            }).result.then(function (taskResponse) {

                if (taskResponse != undefined) {

                    if (taskResponse == "success") {
                        ngToast.create({
                            content: taskResponse,
                            className: "success",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });

                    }
                    else {
                        ngToast.create({
                            content: taskResponse,
                            className: "danger",
                            closeButton: "true",
                            horizontalPosition: "center"
                        });
                    }
                }

            }, function () {

            });
        };

    }]);

app.controller('reportsReconcialtionCtrl', ['$scope', '$window', '$location', "$cookies", "$timeout", "ngToast", "$filter", "$http", "$interval", "$modal",
    function ($scope, $window, $location, $cookies, $timeout, ngToast, $filter, $http, $interval, $modal) {
        var serviceUrlRoot = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        $scope.all_topics = [];
        $scope.inputParam = "";
        $scope.servicePending = false;
        var url = serviceUrlRoot + "/get_topics";
        $http.get(url).then(function (response) {
            $scope.all_topics = response.data;
            $scope.servicePending = true;
        });

    }]);
