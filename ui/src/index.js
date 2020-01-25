import { Route, Switch } from 'wouter-preact';
import { Provider } from 'redux-zero/preact';

import './style';

import store from './store';
import Navbar from './components/navbar';
import Home from './views/home';

export default function App() {
  return (
    <div id="app">
      <Provider store={store}>
        <Navbar />
      </Provider>
      <Switch>
        <Route path="/" component={Home} />
      </Switch>
    </div>
  );
}
