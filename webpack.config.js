const path=require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');

let files=[];
fs.readdirSync('./src/pages/').forEach(file => {
    if (path.extname(file)=='.html'){
        files.push(file);
    }
});

let multipleHtmlPlugins=files.map(file => {
    return new HtmlWebpackPlugin({
        template: `./src/pages/${file.name}.html`,
        filemame: `./dist/${file.name}.html`,
        favicon: './src/assets/img/favicon.ico',
        meta: {
            viewport: 'width=device-width, initial-scale=1',
            charset: 'utf-8'
        }
    })
})

module.exports={
    entry: './src/index.js',
    mode: 'development',
    output:{
        path: path.resolve(__dirname, './dist/'),
        filename: 'bundle.js'
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
            favicon: './src/assets/img/favicon.ico',
            meta: {
                viewport: 'width=device-width, initial-scale=1',
                charset: 'utf-8'
            }
        }).concat(multipleHtmlPlugins)
    ]
}
