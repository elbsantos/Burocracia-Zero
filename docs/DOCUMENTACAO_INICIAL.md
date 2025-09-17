# Documentação Inicial – Burocracia Zero
Estrutura sugerida da pasta /docs
docs/
├─ user-stories.md
├─ wireframes.md
├─ api-whatsapp.md
├─ data-structure.md
└─ roadmap.md

# 1 - User Stories – MVP

## Cadastro de Empresa/Freelancer
- **Como** microempresário ou freelancer
- **Quero** cadastrar minha empresa ou perfil
- **Para** receber faturas, lembretes e acessar meus documentos

Campos:
- Nome da empresa/freelancer
- NIF
- E-mail
- WhatsApp

---

## Geração de Fatura/Recibo
- **Como** usuário
- **Quero** gerar faturas ou recibos em PDF
- **Para** cumprir minhas obrigações fiscais rapidamente

Integração:
- e-Fatura (Portugal)

---

## Lembretes de Obrigações Fiscais
- **Como** usuário
- **Quero** receber notificações via WhatsApp
- **Para** não perder prazos de vencimento de recibos ou contratos

---

## Assinatura Digital
- **Como** usuário
- **Quero** assinar contratos ou documentos digitalmente
- **Para** formalizar acordos sem sair do WhatsApp

---

## Upload e Armazenamento de Documentos
- **Como** usuário
- **Quero** armazenar documentos de forma segura
- **Para** acessar ou compartilhar rapidamente

---

## Chatbot WhatsApp
- **Como** usuário
- **Quero** interagir com comandos básicos via WhatsApp
- **Exemplos:** "gerar recibo", "enviar documento", "meus lembretes"

# 2 - Wireframes – MVP

## Painel Web
1. **Dashboard**
   - Lista de faturas/recibos/contratos
   - Status de documentos
   - Lembretes próximos
2. **Cadastro**
   - Formulário de cadastro de empresa/freelancer
3. **Upload de Documentos**
   - Interface simples para arrastar e soltar arquivos
4. **Histórico de Transações**
   - Lista de documentos enviados, recebidos e gerados

## WhatsApp
- Comandos principais do chatbot:
  - "gerar recibo"
  - "enviar documento"
  - "meus lembretes"

# 3 - Integração WhatsApp – MVP

## Serviços Sugeridos
- Twilio API ou Z-API
- Funções principais:
  1. Envio de mensagens automáticas
  2. Recebimento de mensagens para chatbot
  3. Envio de PDFs ou links seguros

## Comandos do Chatbot
| Comando             | Descrição                                    |
|---------------------|----------------------------------------------|
| gerar recibo        | Gera um recibo PDF e envia ao usuário        |
| enviar documento    | Envia documento para o usuário ou contador   |
| meus lembretes      | Lista lembretes fiscais do usuário           |

## Fluxo
1. Usuário envia comando → WhatsApp API  
2. Backend processa comando → gera arquivo ou busca dados  
3. Backend envia resposta via API → usuário recebe no WhatsApp

# 4 - Estrutura de Dados – MVP

## Usuário/Empresa
```json
{
  "nome": "Nome da empresa ou freelancer",
  "nif": "Número de identificação fiscal",
  "email": "email@exemplo.com",
  "whatsapp": "+351900000000",
  "documentos": [
    {
      "tipo": "recibo",
      "nome_arquivo": "recibo_001.pdf",
      "data_criacao": "2025-09-16"
    }
  ]
}

# 5 - Documento Fatura

{
  "tipo": "fatura | recibo",
  "numero": "001",
  "cliente": "Nome do cliente",
  "valor": 100.0,
  "data_emissao": "2025-09-16",
  "pdf_link": "https://s3.amazon.com/recibo_001.pdf"
}

# 6 - Roadmap Inicial – MVP

## Fase 1 – MVP (prioridade máxima)
- Cadastro de empresa/freelancer
- Geração de fatura/recibo PDF
- Lembretes via WhatsApp
- Assinatura digital básica
- Upload e armazenamento seguro
- Painel web simples
- Chatbot WhatsApp com comandos básicos

## Fase 2 – Funcionalidades futuras
- Leitura automática de documentos (OCR/IA)
- Integração direta com contabilistas
- Suporte a outros mensageiros (Telegram, Signal)
- Melhorias em UI/UX do painel web
- Conformidade GDPR e eIDAS completa
