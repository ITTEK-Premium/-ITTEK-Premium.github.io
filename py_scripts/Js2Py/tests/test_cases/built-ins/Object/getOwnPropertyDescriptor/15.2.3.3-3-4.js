// Copyright (c) 2012 Ecma International.  All rights reserved.
// Ecma International makes this code available under the terms and conditions set
// forth on http://hg.ecmascript.org/tests/test262/raw-file/tip/LICENSE (the
// "Use Terms").   Any redistribution of this code must retain the above
// copyright and this notice and otherwise comply with the Use Terms.

/*---
es5id: 15.2.3.3-3-4
description: >
    Object.getOwnPropertyDescriptor - 'P' is own data property that
    overrides an inherited accessor property
includes: [runTestCase.js]
---*/

function testcase() {

        var proto = {};
        Object.defineProperty(proto, "property", {
            get: function () {
                return "inheritedDataProperty";
            },
            configurable: true
        });

        var Con = function () { };
        Con.ptototype = proto;

        var child = new Con();
        Object.defineProperty(child, "property", {
            value: "ownDataProperty",
            configurable: true
        });

        var desc = Object.getOwnPropertyDescriptor(child, "property");

        return desc.value === "ownDataProperty";
    }
runTestCase(testcase);
