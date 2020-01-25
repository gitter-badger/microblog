import { Route } from 'wouter-preact';
import { Provider } from 'redux-zero/preact';

import './style';

import store from './store';
import Navbar from './components/navbar';
import Home from './views/home';
import Login from './views/login';

export default function App() {
  return (
    <div id="app">
      <Provider store={store}>
        <Navbar />
      </Provider>
      <Route path="/" component={Home} />
      <Route path="/login">
        <Provider store={store}>
          <Login />
        </Provider>
      </Route>
    </div>
  );
}
