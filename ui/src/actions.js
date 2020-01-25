const actions = (_store) => ({
  setUser: (_state, newUser) => ({ user: newUser }),
  clearUser: (_state) => ({ user: null }),
  setToken: (_state, newToken) => ({ token: newToken }),
  clearToken: (_state) => ({ token: null })
});

export default actions;
