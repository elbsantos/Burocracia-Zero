import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <div>
        <nav style={{ padding: '10px', background: '#f0f0f0', borderBottom: '1px solid #ccc' }}>
          <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0, gap: '20px' }}>
            <li><Link to="/">Página Inicial</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Registo</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
          </ul>
        </nav>

        <hr />

        <div style={{ padding: '20px' }}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* Rota Protegida para o Dashboard e todas as suas sub-rotas */}
            <Route 
              path="/dashboard/*" // O '*' é crucial para as rotas aninhadas
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              } 
            />

            <Route path="/" element={
              <div>
                <h2>Página Inicial</h2>
                <p>Bem-vindo ao BurocraciaZero!</p>
              </div>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
