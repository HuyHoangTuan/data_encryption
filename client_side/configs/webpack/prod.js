// Copyright (c) Meta Platforms, Inc. and affiliates.
// All rights reserved.

// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

// production config
const { merge } = require("webpack-merge");
const { resolve } = require("path");
const commonConfig = require("./common");

module.exports = merge(commonConfig, {
  mode: "production",
  output: {
    filename: "static/js/bundle.min.js",
    path: resolve(__dirname, "../../../public"),
    publicPath: '/'
  }, 
});
