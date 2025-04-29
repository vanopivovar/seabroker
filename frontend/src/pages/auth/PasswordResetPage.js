import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const PasswordResetPage = () => {
  const { uid, token } = useParams();
  const navigate = useNavigate();
  const { requestPasswordReset, confirmPasswordReset } = useAuth();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isConfirming, setIsConfirming] = useState(false);
  
  useEffect(() => {
    // Check if we're in confirm password reset mode (with uid and token)
    if (uid && token) {
      setIsConfirming(true);
    }
  }, [uid, token]);
  
  const handleRequestReset = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setLoading(true);
    
    try {
      await requestPasswordReset(email);
      setMessage('Инструкции по сбросу пароля отправлены на ваш email');
      setEmail('');
    } catch (err) {
      setError('Не удалось отправить инструкции. Проверьте корректность email');
      console.error('Password reset request error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleConfirmReset = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    if (password !== confirmPassword) {
      return setError('Пароли не совпадают');
    }
    
    setLoading(true);
    
    try {
      await confirmPasswordReset(uid, token, password);
      setMessage('Пароль успешно изменен');
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err) {
      setError('Не удалось сбросить пароль. Ссылка может быть недействительной или просроченной');
      console.error('Password reset confirmation error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="row justify-content-center">
      <div className="col-md-6 col-lg-4">
        <div className="card shadow">
          <div className="card-body p-4">
            <h2 className="text-center mb-4">
              {isConfirming ? 'Создание нового пароля' : 'Сброс пароля'}
            </h2>
            
            {message && <div className="alert alert-success">{message}</div>}
            {error && <div className="alert alert-danger">{error}</div>}
            
            {isConfirming ? (
              <form onSubmit={handleConfirmReset}>
                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Новый пароль</label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label htmlFor="confirmPassword" className="form-label">Подтверждение пароля</label>
                  <input
                    type="password"
                    className="form-control"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
                
                <button 
                  type="submit" 
                  className="btn btn-primary w-100 mt-3" 
                  disabled={loading}
                >
                  {loading ? 'Обработка...' : 'Установить новый пароль'}
                </button>
              </form>
            ) : (
              <form onSubmit={handleRequestReset}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                
                <button 
                  type="submit" 
                  className="btn btn-primary w-100 mt-3" 
                  disabled={loading}
                >
                  {loading ? 'Отправка...' : 'Отправить инструкции по сбросу'}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PasswordResetPage;