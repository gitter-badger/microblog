import { Link } from 'wouter-preact';
import { Connect } from 'redux-zero/preact';

const mapToProps = ({ user }) => ({ user });

function AccountLink({ user }) {
  if (user) {
    return <Link href="/account" class="btn btn-link">Account</Link>;
  }
  return <Link href="/login" class="btn btn-link">Login</Link>;
}

const Navbar = () => (
  <Connect mapToProps={mapToProps}>
    {({ user }) => (
      <header class="navbar">
        <section class="navbar-section">
          <Link href="/" class="navbar-brand mr-2">Microblog</Link>
        </section>
        <section class="navbar-section">
          <AccountLink user={user} />
        </section>
      </header>
    )}
  </Connect>
);

export default Navbar;
