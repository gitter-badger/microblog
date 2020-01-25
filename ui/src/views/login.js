import { Component } from 'preact';
import { connect } from 'redux-zero/preact';
import { useLocation } from 'wouter-preact';

import actions from '../actions';
import Bus from '../utils/Bus';

const mapToProps = ({ user, token }) => ({ user, token });

class LoginBase extends Component {
  state = { name: '', password: '' };

  onSubmit = (e) => {
    const errcodeMap = {
      400: 'Invalid data submitted',
      404: 'No account with that credentials found'
    };
    const url = '/api/login';
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: this.state.name, password: this.state.password })
    })
      .then((resp) => {
        if (resp.ok) {
          return resp.json();
        }
        return Promise.reject({ status: resp.status, statusText: resp.statusText });
      })
      .then((data) => {
        const userObj = {
          name: data.name,
          pk: data.pk,
          slug: data.slug
        };
        this.setUser(userObj);
        this.setToken(data.token);
        this.redirect('/');
      })
      .catch((err) => {
        const msg = errcodeMap[err.status];
        Bus.emit('flash', ({ message: msg, type: 'error' }));
      });
    e.preventDefault();
  }

  onInputName = (e) => {
    this.setState({ name: e.target.value });
  }

  onInputPassword = (e) => {
    this.setState({ password: e.target.value });
  }

  constructor({ setUser, setToken }) {
    super();
    this.setUser = setUser;
    this.setToken = setToken;
    const [, setLocation] = useLocation();
    this.redirect = setLocation;
  }

  render(_, { name, password }) {
    return (
      <form class="form-horizontal" onSubmit={this.onSubmit}>
        <div class="form-group">
          <div class="col-3 col-sm-12">
            <label class="form-label" for="input-name">Name</label>
          </div>
          <div class="col-9 col-sm-12">
            <input
              class="form-input" type="text" id="input-name" name="name" placeholder="User name" value={name}
              onInput={this.onInputName}
            />
          </div>
        </div>
        <div class="form-group">
          <div class="col-3 col-sm-12">
            <label class="form-label" for="input-password">Password</label>
          </div>
          <div class="col-9 col-sm-12">
            <input
              class="form-input" type="password" id="input-password" name="password" value={password}
              onInput={this.onInputPassword}
            />
          </div>
        </div>
        <div class="form-group">
          <div class="col-9 col-ml-auto">
            <button class="btn btn-primary" type="submit">Login</button>
          </div>
        </div>
      </form>
    );
  }
}

const Login = connect(mapToProps, actions)(LoginBase);

export default Login;
