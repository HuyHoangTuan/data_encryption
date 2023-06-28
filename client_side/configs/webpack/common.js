// Copyright (c) Meta Platforms, Inc. and affiliates.
// All rights reserved.

// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

const {resolve} = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const FriendlyErrorsWebpackPlugin = require("friendly-errors-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const webpack = require("webpack");
require('dotenv').config({path: '../.env'});
const path = require('path');

module.exports = {
    entry: path.resolve(__dirname, "../../src/index.js"),
    stats: {
        assets: false,
        chunks: false,
        chunkGroups: false,
        chunkModules: false,
        chunkOrigins: false,
        entrypoints: false,
        modules: false,
        moduleTrace: false,
        providedExports: false,
        usedExports: false,
        optimizationBailout: false,
        performance: false,
        publicPath: false,
        reasons: false,
        source: false,
        timings: false,
        version: false,
        warnings: true,
    },
    resolve: {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
            },
        ],
    },
    plugins: [
        new CopyPlugin({
            patterns: [
                {
                    from: "static",
                    to: "../public/static",
                    globOptions: {
                        ignore: ['**/index.html']  // Ignore specific files/patterns
                    }
                },
            ],
        }),
        new HtmlWebpackPlugin({
            template: "./static/index.html",
        }),
        new FriendlyErrorsWebpackPlugin(),
        new webpack.DefinePlugin({
            "process.env": JSON.stringify(process.env),
        }),
        new webpack.ProvidePlugin({
            process: "process/browser",
        }),
    ],
};
