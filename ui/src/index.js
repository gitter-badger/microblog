import { Component } from 'preact';
import { Router } from 'preact-router';

import './style';

import Home from './views/home';
import Profile from './views/profile';

export default class App extends Component {
	
	handleRoute = (e) => {
		this.currentUrl = e.url;
	};

	render() {
		return (
			<div id="app">
				<Router onChange={this.handleRoute}>
					<Home path="/" />
					<Profile path="/profile/" user="me" />
					<Profile path="/profile/:user" />
				</Router>
			</div>
		);
	}
}
