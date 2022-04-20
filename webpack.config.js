const path=require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');

function generateHTML(){
    const pages=fs.readdirSync(path.resolve(__dirname, './src/pages'))
    pages.unshift('index.html');
    const htmlPages=pages.filter(page => path.extname(page)=='.html');
    return htmlPages.map(item => {
        const name=item.split('.')[0]
        if(name=='index'){
            return new HtmlWebpackPlugin({
                template: './src/index.html',
                filename: 'index.html',
                favicon: './src/assets/img/favicon.ico',
                chunks: ['main'],
                meta: {
                    viewport: 'width=device-width, initial-scale=1',
                }
            })
        }
        return new HtmlWebpackPlugin({
            filename: `${name}.html`,
            template: `./src/pages/${name}.html`,
            favicon: './src/assets/img/favicon.ico',
            chunks: [`${name}`],
            meta: {
                viewport: 'width=device-width, initial-scale=1',
            }
        })
    })
}
const generatedHTML=generateHTML();

module.exports={
    entry: './src/index.js',
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
    ].concat(generatedHTML)
}
