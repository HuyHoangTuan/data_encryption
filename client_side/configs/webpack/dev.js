﻿const { merge } = require("webpack-merge");
const commonConfig = require("./common");
const path = require('path');

module.exports = merge(commonConfig, {
    mode: "development",
    devServer: {
        port: process.env.REACT_APP_PORT,
        static: {
            directory: path.join(__dirname, '../../static'),
            publicPath: '/static'
        },
        hot: true, // enable HMR on the server
        open: true,
        // These headers enable the cross origin isolation state
        // needed to enable use of SharedArrayBuffer for ONNX 
        // multithreading. 
        headers: {
            "Cache-Control": "public, max-age=3600",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Embedder-Policy": "credentialless",
        },
    },
    devtool: "cheap-module-source-map",
});