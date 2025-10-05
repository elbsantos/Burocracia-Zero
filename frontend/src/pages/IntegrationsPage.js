// frontend/src/pages/IntegrationsPage.js
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../services/api';

function IntegrationsPage() {
  const [searchParams] = useSearchParams();
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const status = searchParams.get('status');
    if (status === 'success') {
      setConnectionStatus('Conectado com sucesso!');
    } else if (status === 'error') {
      const details = searchParams.get('details');
      setConnectionStatus(`Falha na conexão: ${details || 'Tente novamente.'}`);
    }

    const fetchUser = async () => {
      setIsLoading(true);
      try {
        const response = await api.get('/users/me/');
        setUser(response.data);
      } catch (error) {
        console.error("Não foi possível ir buscar os dados do utilizador", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchUser();
  }, [searchParams]);

  const handleConnect = async () => {
    try {
      const response = await api.get('/integrations/moloni/connect/');
      const { authorization_url } = response.data;
      if (authorization_url) {
        window.location.href = authorization_url;
      } else {
        throw new Error("URL de autorização não recebida.");
      }
    } catch (error) {
      console.error("Não foi possível iniciar a conexão com o Moloni:", error);
      alert("Ocorreu um erro ao tentar conectar com o Moloni.");
    }
  };

  if (isLoading) {
    return <div>A carregar dados da integração...</div>;
  }

  return (
    <div>
      <h2>Integrações</h2>
      
      {connectionStatus && <p style={{ color: connectionStatus.includes('sucesso') ? 'green' : 'red', fontWeight: 'bold' }}>{connectionStatus}</p>}

      <div>
        <h3>Moloni</h3>
        {user && user.moloni_access_token ? (
          <p style={{ color: 'green' }}>A sua conta está conectada ao Moloni.</p>
        ) : (
          <div>
            <p>Conecte a sua conta do Moloni para emitir faturas certificadas.</p>
            <button onClick={handleConnect}>Ligar ao Moloni</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default IntegrationsPage;
