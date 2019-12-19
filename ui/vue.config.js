module.exports = {
  devServer: {
    proxy: {
      '/*': {
        target: 'http://127.0.0.1:5000',
        secure: false,
      },
    },
  },
};
