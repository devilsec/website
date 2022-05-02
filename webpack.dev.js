const {merge} = require('webpack-merge');
const common = require('./webpack.common');
const ESLintPlugin = require('eslint-webpack-plugin');

module.exports=merge(common, {
  mode:    'development',
  devtool: 'source-map',
  stats:   {
    env:           true,
    outputPath:    true,
    publicPath:    true,
    children:      true,
    logging:       true,
    loggingTrace:  true,
    warnings:      true,
    errors:        true,
    errorDetails:  true,
    errorStack:    true,
    moduleTrace:   true,
    builtAt:       true,
    errorsCount:   true,
    warningsCount: true,
    timings:       true,
    version:       true,
    hash:          true
  },
  devServer: {
    port:     8080,
    https:    true,
    compress: false,
    hot:      true,
    open:     true
  },
  plugins: [
    new ESLintPlugin()
  ]
});
