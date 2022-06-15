// Copyright (c) 2012 Ecma International.  All rights reserved.
// Ecma International makes this code available under the terms and conditions set
// forth on http://hg.ecmascript.org/tests/test262/raw-file/tip/LICENSE (the
// "Use Terms").   Any redistribution of this code must retain the above
// copyright and this notice and otherwise comply with the Use Terms.

/*---
es5id: 15.4.4.15-2-7
description: >
    Array.prototype.lastIndexOf - 'length' is own accessor property on
    an Array-like object
includes: [runTestCase.js]
---*/

function testcase() {

        var obj = { 1: true, 2: false };

        Object.defineProperty(obj, "length", {
            get: function () {
                return 2;
            },
            configurable: true
        });

        return Array.prototype.lastIndexOf.call(obj, true) === 1 &&
            Array.prototype.lastIndexOf.call(obj, false) === -1;
    }
runTestCase(testcase);
