import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { setAuthToken } from '../services/api';
import ClientsPage from './ClientsPage'; // Importar a página de clientes

// Componente para a página de boas-vindas do Dashboard
function DashboardWelcome() {
  return (
    <div>
      <h3>Bem-vindo ao seu painel de controlo!</h3>
      <p>Use o menu à esquerda para navegar pelas funcionalidades.</p>
    </div>
  );
}

// Componente para a futura página de faturas
function InvoicesPagePlaceholder() {
  return <div>Página de Faturas (em construção)</div>;
}

function DashboardPage() {
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setAuthToken(null);
    window.location.href = '/login';
  };

  // Estilo para o link ativo
  const getLinkStyle = (path) => ({
    color: location.pathname.includes(path) ? 'blue' : 'black',
    textDecoration: 'none'
  });

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      {/* Menu Lateral do Dashboard */}
      <div style={{ width: '200px', borderRight: '1px solid #ccc', paddingRight: '20px' }}>
        <h3>Menu</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/clients" style={getLinkStyle('/clients')}>Meus Clientes</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/invoices" style={getLinkStyle('/invoices')}>Minhas Faturas</Link>
          </li>
        </ul>
        <button onClick={handleLogout} style={{ marginTop: '20px', width: '100%' }}>Logout</button>
      </div>

      {/* Área de Conteúdo Principal */}
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<DashboardWelcome />} />
          <Route path="clients" element={<ClientsPage />} />
          <Route path="invoices" element={<InvoicesPagePlaceholder />} />
        </Routes>
      </div>
    </div>
  );
}

export default DashboardPage;
