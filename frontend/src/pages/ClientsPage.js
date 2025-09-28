// frontend/src/pages/ClientsPage.js

import React, { useState, useEffect } from 'react';
import api from '../services/api';

function ClientsPage() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newClient, setNewClient] = useState({ name: '', nif: '', address: '', email: '' });

  // Estado para gerir qual cliente está a ser editado
  const [editingClient, setEditingClient] = useState(null);
  const [editFormData, setEditFormData] = useState({});

  // --- FUNÇÕES PRINCIPAIS ---

  const fetchClients = async () => {
    // Não resetamos o loading aqui para evitar piscar
    try {
      const response = await api.get('/invoicing/clients/');
      setClients(response.data);
    } catch (error) {
      console.error("Não foi possível ir buscar os clientes:", error);
      alert("Ocorreu um erro ao ir buscar os seus clientes.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  // --- FUNÇÕES PARA O FORMULÁRIO DE NOVO CLIENTE ---

  const handleNewClientChange = (e) => {
    setNewClient({
      ...newClient,
      [e.target.name]: e.target.value
    });
  };

  const handleNewClientSubmit = async (e) => {
    e.preventDefault();
    if (!newClient.name) {
      alert("O nome do cliente é obrigatório.");
      return;
    }
    try {
      await api.post('/invoicing/clients/', newClient);
      alert("Cliente adicionado com sucesso!");
      setNewClient({ name: '', nif: '', address: '', email: '' });
      fetchClients(); // Atualiza a lista
    } catch (error) {
      console.error("Erro ao adicionar cliente:", error.response ? error.response.data : "Erro desconhecido");
      alert("Ocorreu um erro ao adicionar o cliente.");
    }
  };

  // --- FUNÇÕES PARA EDIÇÃO ---

  const handleEditClick = (client) => {
    setEditingClient(client);
    setEditFormData(client);
  };

  const handleCancelEdit = () => {
    setEditingClient(null);
    setEditFormData({});
  };

  const handleEditFormChange = (e) => {
    setEditFormData({
      ...editFormData,
      [e.target.name]: e.target.value
    });
  };

  const handleUpdateClient = async (e) => {
    e.preventDefault();
    try {
      await api.patch(`/invoicing/clients/${editingClient.id}/`, editFormData);
      alert("Cliente atualizado com sucesso!");
      setEditingClient(null);
      fetchClients();
    } catch (error) {
      console.error("Erro ao atualizar cliente:", error.response ? error.response.data : "Erro desconhecido");
      alert("Ocorreu um erro ao atualizar o cliente.");
    }
  };

  // --- FUNÇÃO PARA APAGAR ---

  const handleDeleteClient = async (clientId) => {
    if (window.confirm("Tem a certeza que deseja apagar este cliente? Esta ação não pode ser desfeita.")) {
      try {
        await api.delete(`/invoicing/clients/${clientId}/`);
        alert("Cliente apagado com sucesso!");
        fetchClients();
      } catch (error) {
        console.error("Erro ao apagar cliente:", error.response ? error.response.data : "Erro desconhecido");
        alert("Ocorreu um erro ao apagar o cliente.");
      }
    }
  };

  // --- RENDERIZAÇÃO ---

  if (loading) {
    return <div>A carregar clientes...</div>;
  }

  return (
    <div>
      <h2>Meus Clientes</h2>
      
      <div style={{ background: '#f9f9f9', padding: '15px', borderRadius: '5px', marginBottom: '20px' }}>
        <h3>Adicionar Novo Cliente</h3>
        <form onSubmit={handleNewClientSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <label>Nome: </label>
            <input type="text" name="name" value={newClient.name} onChange={handleNewClientChange} required style={{ width: '300px' }} />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>NIF: </label>
            <input type="text" name="nif" value={newClient.nif} onChange={handleNewClientChange} style={{ width: '300px' }} />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Email: </label>
            <input type="email" name="email" value={newClient.email} onChange={handleNewClientChange} style={{ width: '300px' }} />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Morada: </label>
            <textarea name="address" value={newClient.address} onChange={handleNewClientChange} style={{ width: '300px', minHeight: '60px' }} />
          </div>
          <button type="submit">Adicionar Cliente</button>
        </form>
      </div>

      <hr style={{ margin: '20px 0' }} />

      <h3>Lista de Clientes</h3>
      {clients.length > 0 ? (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {clients.map(client => (
            <li key={client.id} style={{ border: '1px solid #eee', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
              {editingClient && editingClient.id === client.id ? (
                <form onSubmit={handleUpdateClient}>
                  <div style={{ marginBottom: '10px' }}><label>Nome: </label><input type="text" name="name" value={editFormData.name} onChange={handleEditFormChange} required /></div>
                  <div style={{ marginBottom: '10px' }}><label>NIF: </label><input type="text" name="nif" value={editFormData.nif} onChange={handleEditFormChange} /></div>
                  <div style={{ marginBottom: '10px' }}><label>Email: </label><input type="email" name="email" value={editFormData.email} onChange={handleEditFormChange} /></div>
                  <div style={{ marginBottom: '10px' }}><label>Morada: </label><textarea name="address" value={editFormData.address} onChange={handleEditFormChange} /></div>
                  <button type="submit">Guardar</button>
                  <button type="button" onClick={handleCancelEdit} style={{ marginLeft: '10px' }}>Cancelar</button>
                </form>
              ) : (
                <div>
                  <strong>{client.name}</strong>
                  <p style={{ margin: '5px 0' }}>NIF: {client.nif || 'N/A'}</p>
                  <p style={{ margin: '5px 0' }}>Email: {client.email || 'N/A'}</p>
                  <button onClick={() => handleEditClick(client)}>Editar</button>
                  <button onClick={() => handleDeleteClient(client.id)} style={{ marginLeft: '10px', background: '#ffdddd', color: '#c00' }}>Apagar</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>Você ainda não tem clientes registados.</p>
      )}
    </div>
  );
}

export default ClientsPage;
