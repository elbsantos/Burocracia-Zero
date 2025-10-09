// frontend/src/pages/DashboardPage.js
import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import api from '../services/api'; // Corrigido: importação do api

import ClientsPage from './ClientsPage';
import InvoiceCreatePage from './InvoiceCreatePage';
import InvoicesListPage from './InvoicesListPage';
import IntegrationsPage from './IntegrationsPage';
import SigningPage from './SigningPage';

function DashboardWelcome() {
  return <h2>Bem-vindo ao seu Dashboard!</h2>;
}

function DashboardPage() {
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    delete api.defaults.headers.common['Authorization'];
    window.location.href = '/login';
  };

  const getLinkStyle = (path) => ({
    fontWeight: location.pathname.includes(path) ? 'bold' : 'normal',
    textDecoration: 'none',
    color: 'black'
  });

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ width: '200px', borderRight: '1px solid #ccc', paddingRight: '20px', flexShrink: 0 }}>
        <h3>Menu</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/clients" style={getLinkStyle('/clients')}>Meus Clientes</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/invoices" style={getLinkStyle('/invoices')}>Minhas Faturas</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/signing" style={getLinkStyle('/signing')}>Assinaturas</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/integrations" style={getLinkStyle('/integrations')}>Integrações</Link>
          </li>
        </ul>
        <button onClick={handleLogout} style={{ marginTop: '20px', width: '100%' }}>Logout</button>
      </div>

      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<DashboardWelcome />} />
          <Route path="clients" element={<ClientsPage />} />
          <Route path="invoices" element={<InvoicesListPage />} />
          <Route path="invoices/new" element={<InvoiceCreatePage />} />
          <Route path="integrations" element={<IntegrationsPage />} />
          <Route path="signing" element={<SigningPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default DashboardPage;
