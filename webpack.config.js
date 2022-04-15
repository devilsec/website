const path=require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');

let files=[];
fs.readdirSync('./src/pages/').forEach(file => {
    if (path.extname(file)=='.html'){
        files.push(file.split('.')[0]);
    }
});

let multipleHtmlPlugins=files.map(file => {
    return new HtmlWebpackPlugin({
        template: `./src/pages/${file}.html`,
        filemame: `${file}.html`,
        favicon: './src/assets/img/favicon.ico',
        chunks: ['main', `${file}`],
        meta: {
            viewport: 'width=device-width, initial-scale=1',
        }
    })
});

module.exports={
    entry: {
        main: './src/components/header.js'
    },
    mode: 'development',
    output:{
        path: path.resolve(__dirname, './dist/'),
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    {loader: 'style-loader'},
                    {loader: 'css-loader'},
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: function(){
                                return[
                                    require('autoprefixer')
                                ];
                            }
                        }
                    },
                    {loader: 'sass-loader'}
                ]
            },
            {
                test: /\.(css)$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html',
            filename: 'index.html',
            favicon: './src/assets/img/favicon.ico',
            chunks: ['main'],
            meta: {
                viewport: 'width=device-width, initial-scale=1',
            }
        })
    ].concat(multipleHtmlPlugins)
}
