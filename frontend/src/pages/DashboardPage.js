import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../services/api';

function DashboardPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // useEffect é um hook que corre quando o componente carrega
  useEffect(() => {
    const fetchUser = async () => {
      try {
        // Tenta ir buscar os dados do utilizador ao endpoint /users/me/
        const response = await api.get('/users/me/');
        setUser(response.data);
      } catch (error) {
        console.error("Não foi possível ir buscar os dados do utilizador", error);
        // Se falhar (ex: refresh token expirou), o interceptor deve tratar do logout
      } finally {
        setLoading(false);
      }
    };

    // Verifica se já existe um token para evitar pedidos desnecessários
    const token = localStorage.getItem('accessToken');
    if (token) {
      setAuthToken(token); // Configura o token no axios ao carregar a página
      fetchUser();
    } else {
      // Se não houver token, não estamos logados, não há nada para carregar
      setLoading(false);
    }
  }, []); // O array vazio [] significa que este efeito corre apenas uma vez

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setAuthToken(null);
    window.location.href = '/login';
  };

  if (loading) {
    return <div>A carregar...</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      {user ? (
        <div>
          <p>Bem-vindo, {user.full_name}! Esta página é protegida.</p>
          <p>Email: {user.email}</p>
          <p>Plano: {user.subscription_plan}</p>
        </div>
      ) : (
        <p>Não foi possível carregar os dados do utilizador. Por favor, faça login.</p>
      )}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default DashboardPage;
