import React, { useState } from 'react';
import api, { setAuthToken } from '../services/api'; // Usar o nosso serviço de API

function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Usar a instância 'api' e o URL relativo
      const response = await api.post('/users/login/', formData);
      
      const { access, refresh } = response.data;

      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);

      // Usar a nossa função centralizada para configurar o token
      setAuthToken(access);

      console.log('Login bem-sucedido!', response.data);
      alert('Login bem-sucedido!');

      // Redirecionar para o dashboard após o login
      window.location.href = '/dashboard';

    } catch (error) {
      console.error('Erro no login:', error.response ? error.response.data : error.message);
      alert('Erro no login. Verifique as suas credenciais.');
    }
  };

  return (
    <div>
      <h1>Página de Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
