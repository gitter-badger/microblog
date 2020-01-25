const actions = (_store) => ({
  setUser: (_state, user) => ({ user }),
  clearUser: (_state) => ({ user: null }),
  setToken: (_state, token) => ({ token }),
  clearToken: (_state) => ({ token: null })
});

export default actions;
