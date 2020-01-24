import { Link } from 'preact-router/match';

const Navbar = () => (
  <header class="navbar">
    <section class="navbar-section">
      <Link href="/" class="navbar-brand mr-2">Microblog</Link>
    </section>
    <section class="navbar-section">
      <Link href="/account" class="btn btn-link">Account</Link>
    </section>
  </header>
);

export default Navbar;
