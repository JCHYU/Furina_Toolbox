const HtmlWebpackPlugin = require('html-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    entry: "./src/index/main.js",
    module: {
        rules: [
            { test:/\.js$/, use: 'babel-loader' },
            { test:/\.vue$/, use: 'vue-loader' },
            { test:/\.css$/, use: ['vue-style-loader', 'css-loader'] },
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index/index.html',
        }),
        new VueLoaderPlugin(),
    ],
};