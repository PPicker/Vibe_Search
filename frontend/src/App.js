import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import ProductDetailPage from './pages/ProductDetailPage';
import SearchPage from './pages/SearchPage';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<SearchPage />} />
                    <Route path="/product/:id" element={<ProductDetailPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
