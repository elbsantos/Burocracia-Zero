# Checklist Visual do MVP - BurocraciaZero

---

## 1. Setup Inicial do Projeto

- [ ] Criar repositório no GitHub
- [ ] Definir estrutura de branches (main/dev/feature)
- [ ] Especificar stack e dependências principais
- [ ] Criar documentação inicial do projeto (README.md)

---

## 2. Cadastro de Empresa/Freelancer

- [ ] Modelar entidades: Empresa, Freelancer, Usuário
- [ ] Implementar API de cadastro (FastAPI/Django)
- [ ] Validação de NIF, e-mail e WhatsApp
- [ ] Tela de cadastro no painel web (React/Next.js)
- [ ] Integração com banco de dados PostgreSQL
- [ ] Autenticação básica (e-mail/senha ou OAuth)

---

## 3. Geração Automática de Fatura/Recibo (PDF + e-fatura)

- [ ] Definir modelo de recibo/fatura (campos obrigatórios)
- [ ] Implementar endpoint para geração de PDF (PDFKit)
- [ ] Tela/formulário de emissão no painel web
- [ ] Salvar PDF gerado no AWS S3
- [ ] Integração inicial com e-fatura (mock ou real)
- [ ] Adicionar link de download do recibo/fatura no painel

---

## 4. Lembrete Fiscal via WhatsApp

- [ ] Criar endpoint para agendamento de lembretes
- [ ] Integração com Twilio API para envio de mensagem WhatsApp
- [ ] Tela para configurar lembretes no painel
- [ ] Teste de envio real para WhatsApp

---

## 5. Assinatura Digital Básica

- [ ] Endpoint para upload de contrato/documento
- [ ] Geração de link único para assinatura digital básica
- [ ] Notificação do link via WhatsApp (Twilio)
- [ ] Registro de assinaturas e status no banco
- [ ] Download do documento assinado no painel

---

## 6. Upload e Armazenamento Seguro de Documentos

- [ ] Tela de upload no painel web
- [ ] Endpoint para upload seguro (FastAPI/Django)
- [ ] Armazenamento no AWS S3
- [ ] Listagem e download de documentos pelo painel

---

## 7. Painel Web Simples (Histórico e Downloads)

- [ ] Login e navegação básica
- [ ] Listagem de recibos/faturas/documentos históricos
- [ ] Botões de download/visualização
- [ ] Interface responsiva (mobile-friendly)

---

## 8. Chatbot WhatsApp (Twilio)

- [ ] Configurar número de teste no Twilio
- [ ] Implementar bot básico: comandos “gerar recibo”, “enviar documento”, “meus lembretes”
- [ ] Conectar endpoints do backend ao bot
- [ ] Testar fluxos principais pelo WhatsApp

---

## 9. Deploy & Infraestrutura

- [ ] Configurar backend para deploy (Railway, Render, AWS, etc)
- [ ] Deploy do frontend (Vercel, Netlify)
- [ ] Configurar domínio e SSL
- [ ] Variáveis de ambiente seguras (.env)

---

## 10. Testes, Validação e Lançamento

- [ ] Testes unitários básicos no backend/frontend
- [ ] Testes de fluxo ponta a ponta
- [ ] Testar com usuários reais (alfa/beta)
- [ ] Landing page para captação de interessados
- [ ] Ajustar MVP conforme feedback inicial

---

## 11. Roadmap Pós-MVP

- [ ] Leitura automática de documentos (OCR/IA)
- [ ] Integração com contabilistas
- [ ] Suporte a Telegram/Signal
- [ ] Conformidade GDPR/eIDAS detalhada

---

### Observações:
- Marque cada tarefa quando concluir.
- Crie Issues/Tasks para dividir cada item em tarefas menores se necessário.