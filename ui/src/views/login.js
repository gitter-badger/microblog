const Login = () => (
  <form class="form-horizontal">
    <div class="form-group">
      <div class="col-3 col-sm-12">
        <label class="form-label" for="input-name">Name</label>
      </div>
      <div class="col-9 col-sm-12">
        <input class="form-input" type="text" id="input-name" placeholder="User name" />
      </div>
    </div>
    <div class="form-group">
      <div class="col-3 col-sm-12">
        <label class="form-label" for="input-password">Password</label>
      </div>
      <div class="col-9 col-sm-12">
        <input class="form-input" type="password" id="input-password" />
      </div>
    </div>
    <div class="form-group">
      <div class="col-9 col-ml-auto">
        <button class="btn btn-primary" type="submit">Login</button>
      </div>
    </div>
  </form>
);

export default Login;
