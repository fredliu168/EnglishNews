/**
 * Created by fred on 2017/5/16.
 */
var $request = {
    del: function (uri, data, successCallback, errorCallback) {
        $.ajax({
            type: 'DELETE',
            url: uri,
            // data to be added to query string:
            data: data,
            // type of data we are expecting in return:
            dataType: 'json',
            //timeout: 30000,
            context: $('body'),
            success: function (data) {
                console.log(data);
                try {
                    if (data['errorCode'] == 10000) {
                        successCallback(data);
                    } else {
                        callErrorCallback(data, errorCallback);
                    }
                } catch (e) {
                    console.log(e);
                    callErrorCallback(data, errorCallback);
                }
            },
            error: function (xhr, type) {
                console.log('Ajax error!');
                callErrorCallback(null, errorCallback);
            }
        })
    },
    get: function (uri, data, successCallback, errorCallback) {
        $.ajax({
            type: 'GET',
            url: uri,
            // data to be added to query string:
            data: data,
            // type of data we are expecting in return:
            dataType: 'json',
            //timeout: 30000,
            context: $('body'),
            success: function (data) {
                console.log(data);
                try {
                     successCallback(data);
                } catch (e) {
                    console.log(e);
                    callErrorCallback(data, errorCallback);
                }
            },
            error: function (xhr, type) {
                console.log('Ajax error!');
                callErrorCallback(null, errorCallback);
            }
        })
    },
    put: function (uri, data, successCallback, errorCallback) {
        $.ajax({
            type: 'PUT',
            url: uri,
            // data to be added to query string:
            data: JSON.stringify(data),
            // type of data we are expecting in return:
            contentType: 'application/json; charset=utf-8',
            //timeout: 30000,
            context: $('body'),
            success: function (data) {
                console.log(data);
                try {
                    if (data['code'] == 10000) {
                        successCallback(data);
                    } else {
                        console.log('callErrorCallback');
                        callErrorCallback(data, errorCallback);
                    }
                } catch (e) {
                    console.log(e);
                    callErrorCallback(data, errorCallback);
                }
            },
            error: function (xhr, type) {
                console.log('Ajax error!');
                callErrorCallback(null, errorCallback);
            }
        })
    },
    post: function (uri, data, successCallback, errorCallback) {
        $.ajax({
             headers: {
                "X-User-Info":"UserMobile=test_python"
            },
            type: 'POST',
            url: uri,
            // data to be added to query string:
            data: JSON.stringify(data),
            // type of data we are expecting in return:
            contentType: 'application/json; charset=utf-8',
            //timeout: 30000,
            context: $('body'),
            success: function (data) {
                console.log(data);
                try {
                    if (data['code'] == 10000) {
                        successCallback(data);
                    } else {
                        console.log('callErrorCallback');
                        callErrorCallback(data, errorCallback);
                    }
                } catch (e) {
                    console.log(e);
                    callErrorCallback(data, errorCallback);
                }
            },
            error: function (xhr, type) {
                console.log('Ajax error!');
                callErrorCallback(null, errorCallback);
            }
        })
    },
    rawPost: function (uri, data, successCallback, errorCallback) {
        $.ajax({
            headers: {
                "X-User-Info":"UserMobile=test_python"
            },
            type: 'POST',
            url: uri,
            // data to be added to query string:
            data: JSON.stringify(data),
            // type of data we are expecting in return:
            contentType: 'application/json; charset=utf-8',
            //timeout: 30000,
            context: $('body'),
            success: function (data) {
                successCallback(data);
            },
            error: function (xhr, type) {
                console.log('Ajax error!');
                callErrorCallback(null, errorCallback);
            }
        })
    }
};

function callErrorCallback(data, callback) {
    if (callback != null && callback != undefined) {
        if (data != null && data['message'] != '') {
            callback(data, data['message']);
        } else {
            callback(data, '获取数据失败');
        }
    }
}