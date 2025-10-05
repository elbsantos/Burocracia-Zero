// frontend/src/pages/InvoiceCreatePage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function InvoiceCreatePage() {
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState('');
  const [items, setItems] = useState([{ description: '', quantity: 1, unit_price: '' }]);
  const [notes, setNotes] = useState('');
  const [documentType, setDocumentType] = useState('FR'); // 'FR' para Fatura-Recibo por defeito
  const navigate = useNavigate();

  // Vai buscar a lista de clientes para preencher o <select>
  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await api.get('/invoicing/clients/');
        setClients(response.data);
      } catch (error) {
        console.error("Não foi possível ir buscar os clientes:", error);
      }
    };
    fetchClients();
  }, []);

  // --- Funções para gerir os itens da fatura ---
  const handleItemChange = (index, event) => {
    const newItems = [...items];
    newItems[index][event.target.name] = event.target.value;
    setItems(newItems);
  };

  const handleAddItem = () => {
    setItems([...items, { description: '', quantity: 1, unit_price: '' }]);
  };

  const handleRemoveItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
  };

  // --- Função para submeter a fatura ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedClient || items.some(item => !item.description || !item.unit_price)) {
      alert("Por favor, selecione um cliente e preencha todos os campos dos itens.");
      return;
    }

    const invoiceData = {
      client: selectedClient,
      document_type: documentType,
      notes: notes,
      items: items.map(item => ({
        description: item.description,
        quantity: parseFloat(item.quantity),
        unit_price: parseFloat(item.unit_price)
      }))
    };

    try {
      await api.post('/invoicing/invoices/', invoiceData);
      alert("Fatura criada com sucesso!");
      navigate('/dashboard/invoices'); // Redireciona para a lista de faturas
    } catch (error) {
      console.error("Erro ao criar fatura:", error.response.data);
      alert("Ocorreu um erro ao criar a fatura.");
    }
  };

  return (
    <div>
      <h2>Criar Nova Fatura</h2>
      <form onSubmit={handleSubmit}>
        {/* Seleção de Cliente */}
        <div>
          <label>Cliente:</label>
          <select value={selectedClient} onChange={(e) => setSelectedClient(e.target.value)} required>
            <option value="">Selecione um cliente</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>{client.name}</option>
            ))}
          </select>
        </div>

        {/* Tipo de Documento */}
        <div>
          <label>Tipo de Documento:</label>
          <select value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
            <option value="FR">Fatura-Recibo</option>
            <option value="FT">Fatura</option>
          </select>
        </div>

        <hr />

        {/* Itens da Fatura */}
        <h3>Itens</h3>
        {items.map((item, index) => (
          <div key={index} style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <input type="text" name="description" placeholder="Descrição" value={item.description} onChange={e => handleItemChange(index, e)} required />
            <input type="number" name="quantity" placeholder="Qtd" value={item.quantity} onChange={e => handleItemChange(index, e)} min="0.01" step="0.01" required />
            <input type="number" name="unit_price" placeholder="Preço Unit." value={item.unit_price} onChange={e => handleItemChange(index, e)} min="0.01" step="0.01" required />
            {items.length > 1 && <button type="button" onClick={() => handleRemoveItem(index)}>Remover</button>}
          </div>
        ))}
        <button type="button" onClick={handleAddItem}>Adicionar Item</button>

        <hr />

        {/* Notas */}
        <div>
          <label>Notas:</label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
        </div>

        {/* Submeter */}
        <button type="submit">Criar Fatura</button>
      </form>
    </div>
  );
}

export default InvoiceCreatePage;
