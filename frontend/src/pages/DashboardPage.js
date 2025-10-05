import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { setAuthToken } from '../services/api';

import ClientsPage from './ClientsPage';
import InvoiceCreatePage from './InvoiceCreatePage';
import InvoicesListPage from './InvoicesListPage';
import IntegrationsPage from './IntegrationsPage'; // Importe a nova página

function DashboardWelcome() { /* ... (sem alterações) ... */ }

function DashboardPage() {
  const location = useLocation();
  const handleLogout = () => { /* ... (sem alterações) ... */ };
  const getLinkStyle = (path) => ({ /* ... (sem alterações) ... */ });

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
          <Route path="integrations" element={<IntegrationsPage />} /> {/* Adicione a nova rota */}
        </Routes>
      </div>
    </div>
  );
}

export default DashboardPage;
