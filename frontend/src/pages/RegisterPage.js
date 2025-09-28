import React, { useState } from 'react';
import api from '../services/api'; // Usar o nosso serviço de API

function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    whatsapp_number: '',
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
      const response = await api.post('/users/register/', formData);
      
      console.log('Resposta da API:', response.data);
      alert('Registo bem-sucedido! Pode agora fazer login.');
      
      // Redirecionar para a página de login após o registo
      window.location.href = '/login';

    } catch (error) {
      console.error('Erro no registo:', error.response ? error.response.data : error.message);
      alert('Erro no registo. Verifique a consola.');
    }
  };

  return (
    <div>
      <h1>Página de Registo</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Nome Completo:</label>
          <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} required />
        </div>
        <div>
          <label>Número de WhatsApp:</label>
          <input type="text" name="whatsapp_number" value={formData.whatsapp_number} onChange={handleChange} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>
        <button type="submit">Registar</button>
      </form>
    </div>
  );
}

export default RegisterPage;
