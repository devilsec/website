const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const InjectBodyPlugin=require('inject-body-webpack-plugin').default;

let entryPoints = {
  main: ['./src/main.js', './src/assets/scss/main.scss']
};

function arrEmpty(arr){
  if(arr.length>0){
    return false;
  }
  return true;
}

function addChunk(name, chunks){
  if(!arrEmpty(chunks)){
    entryPoints[name]=chunks;
  }
}

function getAssets(name){
  let entries=[];
  if(fs.existsSync(`./src/assets/scss/${name}.scss`)){
    entries.push(`./src/assets/scss/${name}.scss`);
  }
  if(fs.existsSync(`./src/assets/js/${name}.js`)){
    entries.push(`./src/assets/js/${name}.js`);
  }
  return entries;
}

function getAssetsDir(dir){
  return [].concat(getAssets(dir)).concat(getAssets(`${dir}/index`));
}

function generateEntryPoints(name){
  let passDirs=[];
  if(name.includes('/')){
    name.split('/').forEach(function(section, index){
      if(index==name.length-1){
        addChunk(`${passDirs.join('.')}.${section}`, getAssets(`${passDirs.join('/')}/${section}`));
      }
      else if(arrEmpty(passDirs)){
        addChunk(section, getAssetsDir(section));
      }
      else{
        addChunk(`${passDirs.join('.')}.${section}`, getAssetsDir(`${passDirs.join('/')}/${section}`));
      }
      passDirs.push(section);
    });
  }
  else{
    addChunk(name, getAssets(name));
  }
}

function getPages(dirPath, pages){
  let files=fs.readdirSync(dirPath);
  pages=pages || [];
  files.forEach(function(file){
    if(fs.statSync(dirPath+'/'+file).isDirectory()){
      pages=getPages(dirPath+'/'+file, pages);
    }
    else{
      pages.push(path.join(__dirname, dirPath, '/', file));
    }
  });
  return pages;
}

function generateChunks(page){
  if(page.includes('/')){
    let chunks=[];
    page.split('/').forEach(function(section){
      if(arrEmpty(chunks)){
        chunks.push(section);
      }
      else{
        chunks.push(`${chunks.at(-1)}.${section}`);
      }
    });
    return ['main'].concat(chunks);
  }
  return ['main', page];
}

function generateHTML(){
  const pages=getPages('./src/pages/');
  pages.unshift('index.html');
  const htmlPages=pages.filter(page => path.extname(page)=='.html');
  return htmlPages.map(item => {
    const name=item.split((__dirname+'/src/pages/')).at(-1).split('.')[0];
    generateEntryPoints(name);
    if(name=='index'){
      return new HtmlWebpackPlugin({
        template: './src/index.html',
        filename: 'index.html',
        favicon:  './src/assets/img/favicon.ico',
        chunks:   ['main', 'index'],
        meta:     {
          viewport: 'width=device-width, initial-scale=1'
        }
      });
    }
    return new HtmlWebpackPlugin({
      filename: `${name}.html`,
      template: `./src/pages/${name}.html`,
      favicon:  './src/assets/img/favicon.ico',
      chunks:   generateChunks(name),
      meta:     {
        viewport: 'width=device-width, initial-scale=1'
      }
    });
  });
}

const generatedHTML=generateHTML();

module.exports={
  entry:  entryPoints,
  mode:   'development',
  output: {
    path:     path.resolve(__dirname, './dist/'),
    filename: '[name].bundle.js',
    clean:    true
  },
  module: {
    rules: [
      {
        test:   /\.html$/,
        loader: 'html-loader'
      },
      {
        test:    /\.js$/,
        exclude: '/node_modules/',
        use:     {loader: 'babel-loader'}
      },
      {
        test: /\.(scss)$/,
        use:  [
          {loader: 'style-loader'}, {loader: 'css-loader'}, {loader: 'resolve-url-loader'}, {loader: 'postcss-loader', options: { sourceMap: true }}, {loader: 'sass-loader', options: { sourceMap: true }}
        ]
      },
      {
        test: /\.(css)$/,
        use:  [
          'style-loader', 'css-loader'
        ]
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource'
      }
    ]
  },
  plugins: [
    new InjectBodyPlugin({
      content:  '<div class="core"><main-header></main-header>',
      position: 'start'
    }),
    new InjectBodyPlugin({
      content:  '<main-footer></main-footer></div>',
      position: 'end'
    })
  ].concat(generatedHTML)
};
