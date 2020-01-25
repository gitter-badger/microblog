const actions = (store) => ({
  setUser: (state, newUser) => ({ user: newUser }),
  clearUser: (state) => ({ user: null }),
  setToken: (state, newToken) => ({ token: newToken }),
  clearToken: (state) => ({ token: null })
});

export default actions;
