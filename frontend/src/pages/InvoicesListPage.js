// frontend/src/pages/InvoicesListPage.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function InvoicesListPage() {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        const response = await api.get('/invoicing/invoices/');
        setInvoices(response.data);
      } catch (error) {
        console.error("Não foi possível ir buscar as faturas:", error);
        alert("Ocorreu um erro ao ir buscar as suas faturas.");
      } finally {
        setLoading(false);
      }
    };

    fetchInvoices();
  }, []);

  if (loading) {
    return <div>A carregar faturas...</div>;
  }

  return (
    <div>
      <h2>Minhas Faturas</h2>
      <Link to="/dashboard/invoices/new" style={{
        display: 'inline-block', padding: '10px 15px', background: 'blue',
        color: 'white', textDecoration: 'none', borderRadius: '5px', marginBottom: '20px'
      }}>
        + Criar Nova Fatura
      </Link>

      {invoices.length > 0 ? (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {invoices.map(invoice => (
            <li key={invoice.id} style={{ border: '1px solid #eee', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
              <strong>{invoice.get_document_type_display || invoice.document_type} #{invoice.id}</strong> para <strong>{invoice.client_name}</strong>
              <p>Data: {new Date(invoice.issue_date).toLocaleDateString()}</p>
              <p>Valor: {invoice.total_amount} €</p>
              <p>Estado: {invoice.status}</p>
              {/* Detalhes dos itens */}
              <ul>
                {invoice.items.map(item => (
                  <li key={item.id}>{item.description} - {item.quantity} x {item.unit_price}€</li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      ) : (
        <p>Você ainda não tem faturas registadas.</p>
      )}
    </div>
  );
}

export default InvoicesListPage;
