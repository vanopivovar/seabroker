import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const VacancyCreatePage = () => {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    requirements: '',
    responsibilities: '',
    location: '',
    salary: '',
    vessel_type: '',
    contract_duration: '',
    start_date: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      // Здесь будет запрос к API для создания вакансии
      console.log('Creating vacancy:', formData);
      
      // Имитация успешного создания
      setTimeout(() => {
        navigate('/vacancies');
      }, 1000);
    } catch (err) {
      setError('Не удалось создать вакансию');
      console.error('Vacancy creation error:', err);
      setLoading(false);
    }
  };
  
  // Проверка, что пользователь - работодатель
  if (currentUser && !currentUser.is_employer) {
    return (
      <div className="alert alert-danger">
        Только работодатели могут создавать вакансии
      </div>
    );
  }
  
  return (
    <div>
      <h1 className="mb-4">Создание вакансии</h1>
      
      {error && <div className="alert alert-danger">{error}</div>}
      
      <div className="card shadow">
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="title" className="form-label">Название должности</label>
              <input
                type="text"
                className="form-control"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="mb-3">
              <label htmlFor="description" className="form-label">Описание вакансии</label>
              <textarea
                className="form-control"
                id="description"
                name="description"
                rows="4"
                value={formData.description}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            
            <div className="mb-3">
              <label htmlFor="requirements" className="form-label">Требования</label>
              <textarea
                className="form-control"
                id="requirements"
                name="requirements"
                rows="3"
                value={formData.requirements}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            
            <div className="mb-3">
              <label htmlFor="responsibilities" className="form-label">Обязанности</label>
              <textarea
                className="form-control"
                id="responsibilities"
                name="responsibilities"
                rows="3"
                value={formData.responsibilities}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            
            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="location" className="form-label">Местоположение</label>
                <input
                  type="text"
                  className="form-control"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="salary" className="form-label">Зарплата</label>
                <input
                  type="text"
                  className="form-control"
                  id="salary"
                  name="salary"
                  value={formData.salary}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
            
            <div className="row">
              <div className="col-md-4 mb-3">
                <label htmlFor="vessel_type" className="form-label">Тип судна</label>
                <select
                  className="form-select"
                  id="vessel_type"
                  name="vessel_type"
                  value={formData.vessel_type}
                  onChange={handleChange}
                  required
                >
                  <option value="">Выберите тип судна</option>
                  <option value="cargo">Сухогруз</option>
                  <option value="tanker">Танкер</option>
                  <option value="passenger">Пассажирское судно</option>
                  <option value="fishing">Рыболовное судно</option>
                  <option value="other">Другое</option>
                </select>
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="contract_duration" className="form-label">Продолжительность контракта</label>
                <input
                  type="text"
                  className="form-control"
                  id="contract_duration"
                  name="contract_duration"
                  value={formData.contract_duration}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="start_date" className="form-label">Дата начала</label>
                <input
                  type="date"
                  className="form-control"
                  id="start_date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleChange}
                />
              </div>
            </div>
            
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <button
                type="button"
                className="btn btn-outline-secondary me-md-2"
                onClick={() => navigate('/vacancies')}
              >
                Отмена
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Сохранение...' : 'Создать вакансию'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default VacancyCreatePage;