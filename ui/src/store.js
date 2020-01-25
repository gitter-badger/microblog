import createStore from 'redux-zero';

const initialState = { user: null, token: null };

const store = createStore(initialState);

export default store;
