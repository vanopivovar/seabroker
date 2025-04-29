import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password1: '',
    password2: '',
    first_name: '',
    last_name: '',
    is_employer: false
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (formData.password1 !== formData.password2) {
      return setError('Пароли не совпадают');
    }
    
    setLoading(true);
    
    try {
      await register({
        email: formData.email,
        password: formData.password1,
        first_name: formData.first_name,
        last_name: formData.last_name,
        is_employer: formData.is_employer,
        is_seaman: !formData.is_employer
      });
      navigate('/');
    } catch (err) {
      setError('Ошибка регистрации. Проверьте введенные данные.');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="row justify-content-center">
      <div className="col-md-8 col-lg-6">
        <div className="card shadow">
          <div className="card-body p-4">
            <h2 className="text-center mb-4">Регистрация</h2>
            
            {error && <div className="alert alert-danger">{error}</div>}
            
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="first_name" className="form-label">Имя</label>
                  <input
                    type="text"
                    className="form-control"
                    id="first_name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="col-md-6 mb-3">
                  <label htmlFor="last_name" className="form-label">Фамилия</label>
                  <input
                    type="text"
                    className="form-control"
                    id="last_name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="mb-3">
                <label htmlFor="password1" className="form-label">Пароль</label>
                <input
                  type="password"
                  className="form-control"
                  id="password1"
                  name="password1"
                  value={formData.password1}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="mb-3">
                <label htmlFor="password2" className="form-label">Подтверждение пароля</label>
                <input
                  type="password"
                  className="form-control"
                  id="password2"
                  name="password2"
                  value={formData.password2}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="mb-3 form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="is_employer"
                  name="is_employer"
                  checked={formData.is_employer}
                  onChange={handleChange}
                />
                <label className="form-check-label" htmlFor="is_employer">
                  Я работодатель
                </label>
              </div>
              
              <div className="mb-3 form-text">
                {formData.is_employer 
                  ? "Вы сможете публиковать вакансии и искать сотрудников" 
                  : "Вы сможете создавать резюме и откликаться на вакансии"}
              </div>
              
              <button 
                type="submit" 
                className="btn btn-primary w-100 mt-3" 
                disabled={loading}
              >
                {loading ? 'Регистрация...' : 'Зарегистрироваться'}
              </button>
            </form>
            
            <hr className="my-4" />
            
            <div className="text-center">
              <p>Уже есть аккаунт? <Link to="/login">Войти</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;