import React from 'react';
import ReactDOM from 'react-dom';
import Routes from './routes';
import * as serviceWorker from './serviceWorker';
import './styles/global-style.css';

ReactDOM.render(<Routes />, document.getElementById('root'));
serviceWorker.register();
