// Copyright (c) 2012 Ecma International.  All rights reserved.
// Ecma International makes this code available under the terms and conditions set
// forth on http://hg.ecmascript.org/tests/test262/raw-file/tip/LICENSE (the
// "Use Terms").   Any redistribution of this code must retain the above
// copyright and this notice and otherwise comply with the Use Terms.

/*---
es5id: 15.4.4.19-8-b-7
description: >
    Array.prototype.map - properties can be added to prototype after
    current position are visited on an Array
includes: [runTestCase.js]
---*/

function testcase() {
        function callbackfn(val, idx, obj) {
            if (idx === 1 && val === 6.99) {
                return false;
            } else {
                return true;
            }
        }
        var arr = [0, , 2];

        try {
            Object.defineProperty(arr, "0", {
                get: function () {
                    Object.defineProperty(Array.prototype, "1", {
                        get: function () {
                            return 6.99;
                        },
                        configurable: true
                    });
                    return 0;
                },
                configurable: true
            });

            var testResult = arr.map(callbackfn);
            return testResult[0] === true && testResult[1] === false;
        } finally {
            delete Array.prototype[1];
        }
    }
runTestCase(testcase);
