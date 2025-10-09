// frontend/src/pages/SigningPage.js
import React, { useState, useEffect } from 'react';
import api from '../services/api';

function SigningPage() {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Estados para o formulário de upload
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [signers, setSigners] = useState([{ name: '', email: '' }]);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  // Função para ir buscar a lista de documentos
  const fetchDocuments = async () => {
    try {
      const response = await api.get('/signing/documents/');
      setDocuments(response.data);
    } catch (err) {
      console.error("Erro ao ir buscar os documentos:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Funções para manipular os signatários no formulário
  const handleSignerChange = (index, event) => {
    const values = [...signers];
    values[index][event.target.name] = event.target.value;
    setSigners(values);
  };

  const addSigner = () => {
    setSigners([...signers, { name: '', email: '' }]);
  };

  const removeSigner = (index) => {
    const values = [...signers];
    values.splice(index, 1);
    setSigners(values);
  };

  // Função para submeter o formulário
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file || !title || signers.some(s => !s.name || !s.email)) {
      setError('Por favor, preencha todos os campos, incluindo o ficheiro e pelo menos um signatário.');
      return;
    }
    
    setIsUploading(true);
    setError('');

    // FormData é necessário para enviar ficheiros (multipart/form-data)
    const formData = new FormData();
    formData.append('title', title);
    formData.append('original_file', file);
    
    // O nosso backend espera que os signers sejam uma string JSON
    formData.append('signers', JSON.stringify(signers.map(s => ({ signer_name: s.name, signer_email: s.email }))));

    try {
      await api.post('/signing/documents/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Limpa o formulário e atualiza a lista
      setTitle('');
      setFile(null);
      setSigners([{ name: '', email: '' }]);
      fetchDocuments(); // Recarrega a lista de documentos
      alert('Documento enviado para assinatura com sucesso!');

    } catch (err) {
      console.error("Erro no upload do documento:", err.response ? err.response.data : err);
      setError('Ocorreu um erro ao enviar o documento. Tente novamente.');
    } finally {
      setIsUploading(false);
    }
  };

  if (isLoading) {
    return <div>A carregar documentos...</div>;
  }

  return (
    <div>
      <h2>Assinatura de Documentos</h2>

      {/* Formulário de Upload */}
      <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px' }}>
        <h3>Enviar Novo Documento para Assinatura</h3>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Título do Documento:</label>  

            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required style={{width: '300px'}}/>
          </div>
          <div style={{marginTop: '10px'}}>
            <label>Ficheiro (PDF):</label>  

            <input type="file" onChange={(e) => setFile(e.target.files[0])} accept=".pdf" required />
          </div>
          
          <h4 style={{marginTop: '15px'}}>Signatários</h4>
          {signers.map((signer, index) => (
            <div key={index} style={{ display: 'flex', gap: '10px', marginBottom: '5px' }}>
              <input type="text" name="name" placeholder="Nome do Signatário" value={signer.name} onChange={e => handleSignerChange(index, e)} required />
              <input type="email" name="email" placeholder="Email do Signatário" value={signer.email} onChange={e => handleSignerChange(index, e)} required />
              <button type="button" onClick={() => removeSigner(index)}>Remover</button>
            </div>
          ))}
          <button type="button" onClick={addSigner} style={{marginTop: '5px'}}>+ Adicionar Signatário</button>
          
          <hr style={{margin: '15px 0'}}/>
          
          <button type="submit" disabled={isUploading}>
            {isUploading ? 'A Enviar...' : 'Enviar para Assinatura'}
          </button>
          {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </form>
      </div>

      {/* Lista de Documentos */}
      <h3>Meus Documentos</h3>
      {documents.length > 0 ? (
        <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{textAlign: 'left', padding: '5px'}}>Título</th>
              <th style={{textAlign: 'left', padding: '5px'}}>Estado</th>
              <th style={{textAlign: 'left', padding: '5px'}}>Data de Criação</th>
              <th style={{textAlign: 'left', padding: '5px'}}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {documents.map(doc => (
              <tr key={doc.id}>
                <td style={{padding: '5px'}}>{doc.title}</td>
                <td style={{padding: '5px'}}>{doc.status}</td>
                <td style={{padding: '5px'}}>{new Date(doc.created_at).toLocaleString('pt-PT')}</td>
                <td style={{padding: '5px'}}>
                  <a href={`http://localhost:8000${doc.original_file_url}`} target="_blank" rel="noopener noreferrer">Ver Original</a>
                </td>
              </tr>
             ))}
          </tbody>
        </table>
      ) : (
        <p>Ainda não enviou nenhum documento para assinatura.</p>
      )}
    </div>
  );
}

export default SigningPage;
