import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);

// 성능 측정을 위한 웹 바이탈스
// 자세한 정보: https://bit.ly/CRA-vitals
reportWebVitals();