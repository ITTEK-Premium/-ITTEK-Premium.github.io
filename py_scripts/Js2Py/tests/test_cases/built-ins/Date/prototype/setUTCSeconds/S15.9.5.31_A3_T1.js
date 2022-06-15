// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
info: >
    The Date.prototype.setUTCSeconds property "length" has { ReadOnly,
    DontDelete, DontEnum } attributes
es5id: 15.9.5.31_A3_T1
description: Checking ReadOnly attribute
---*/

x = Date.prototype.setUTCSeconds.length;
Date.prototype.setUTCSeconds.length = 1;
if (Date.prototype.setUTCSeconds.length !== x) {
  $ERROR('#1: The Date.prototype.setUTCSeconds.length has the attribute ReadOnly');
}
