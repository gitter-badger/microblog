import { Route } from 'wouter-preact';
import { Provider } from 'redux-zero/preact';

import './style';

import store from './store';
import Navbar from './components/navbar';
import Flash from './components/flash';
import Home from './views/home';
import Login from './views/login';
import Bus from './utils/Bus';

if (typeof window !== 'undefined') {
  window.flash = (message, type='primary') => Bus.emit('flash', ({ message, type }));
}

export default function App() {
  return (
    <div id="app">
      <Provider store={store}>
        <Navbar />
      </Provider>
      <Flash />
      <Route path="/" component={Home} />
      <Route path="/login">
        <Provider store={store}>
          <Login />
        </Provider>
      </Route>
    </div>
  );
}
