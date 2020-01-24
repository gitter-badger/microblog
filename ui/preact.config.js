export default (config, _env, _helpers) => {

  if (config.devServer) {
    config.devServer.proxy = [
      {
        path: '/api/**',
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        changeHost: true,
        pathRewrite(path, _request) {
          return '/' + path.replace(/^\/[^/]+\//, '');
        }
      }
    ];
  }

};
