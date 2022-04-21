const path=require('path');
const fs = require('fs');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

let entryPoints = {
    main: ['./src/main.js', './src/assets/scss/main.scss']
};

function generateEntryPoints(name){
    let entries=[];
    if(fs.existsSync(`./src/assets/scss/${name}.scss`)){
        entries.push(`./src/assets/scss/${name}.scss`);
    }
    if(fs.existsSync(`./src/assets/js/${name}.js`)){
        entries.push(`./src/assets/js/${name}.js`);
    }
    if(entries.length>0){
        entryPoints[name]=entries;
    }
}

function generateHTML(){
    const pages=fs.readdirSync(path.resolve(__dirname, './src/pages'))
    pages.unshift('index.html');
    const htmlPages=pages.filter(page => path.extname(page)=='.html');
    return htmlPages.map(item => {
        const name=item.split('.')[0]
        generateEntryPoints(name);
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
            chunks: ['main', name],
            meta: {
                viewport: 'width=device-width, initial-scale=1',
            }
        })
    })
}
const generatedHTML=generateHTML();

module.exports={
    entry: entryPoints,
    mode: 'development',
    output:{
        path: path.resolve(__dirname, './dist/'),
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.html$/,
                loader: 'html-loader'
            },
            {
                test: /\.js$/,
                exclude: '/node_modules/',
                use: {
                    loader: 'babel-loader',
                }
            },
            {
                test: /\.(scss)$/,
                use: [
                    {loader: 'style-loader'},
                    {loader: 'css-loader'},
                    {loader: 'postcss-loader'},
                    {loader: 'sass-loader'}
                ]
            },
            {
                test: /\.(css)$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
            }
        ]
    },
    plugins: [
    ].concat(generatedHTML)
}
