// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
} );

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Interceptor para tratar de respostas de erro
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Verifica se o erro é 401 e se ainda não tentámos refrescar
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (refreshToken) {
        console.log("Access token expirado. A tentar refrescar...");
        try {
          // Criamos uma nova instância do axios SÓ para este pedido,
          // para evitar problemas de loop do interceptor.
          const refreshResponse = await axios.post('http://localhost:8000/api/users/login/refresh/', {
            refresh: refreshToken
          } );
          
          const { access } = refreshResponse.data;
          
          console.log("Novo access token obtido!");
          localStorage.setItem('accessToken', access);
          setAuthToken(access);
          
          // Atualiza o cabeçalho do pedido original e tenta novamente
          originalRequest.headers['Authorization'] = `Bearer ${access}`;
          return api(originalRequest);

        } catch (refreshError) {
          console.error("Refresh token inválido ou expirado. A fazer logout.", refreshError.response.data);
          setAuthToken(null);
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        console.log("Não há refresh token, a fazer logout.");
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
