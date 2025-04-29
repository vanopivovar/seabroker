import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const VacancyDetailPage = () => {
  const { id } = useParams();
  const { currentUser } = useAuth();
  const [vacancy, setVacancy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [applying, setApplying] = useState(false);
  
  useEffect(() => {
    // Здесь будет фактический запрос к API за данными вакансии
    // Временно используем заглушку
    setTimeout(() => {
      setVacancy({
        id: parseInt(id),
        title: 'Капитан судна',
        company: 'Морские линии',
        location: 'Санкт-Петербург',
        salary: '200000 руб.',
        description: 'Требуется опытный капитан для работы на грузовом судне. Международные рейсы. Опыт работы от 5 лет.',
        requirements: 'Высшее морское образование. Знание английского языка. Опыт работы капитаном от 5 лет.',
        responsibilities: 'Управление судном. Контроль за работой экипажа. Обеспечение безопасности.',
        employer: {
          id: 1,
          name: 'ООО "Морские линии"',
          email: 'info@morlines.ru'
        },
        created_at: '2023-01-15'
      });
      setLoading(false);
    }, 500);
  }, [id]);
  
  const handleApply = () => {
    setApplying(true);
    // Здесь будет запрос к API для создания заявки
    setTimeout(() => {
      alert('Ваша заявка отправлена!');
      setApplying(false);
    }, 1000);
  };
  
  if (loading) {
    return <div className="text-center py-5"><div className="spinner-border"></div></div>;
  }
  
  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }
  
  if (!vacancy) {
    return <div className="alert alert-warning">Вакансия не найдена</div>;
  }
  
  return (
    <div>
      <div className="mb-4">
        <Link to="/vacancies" className="btn btn-outline-secondary">
          &larr; Назад к списку вакансий
        </Link>
      </div>
      
      <div className="card shadow">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h1 className="card-title mb-0">{vacancy.title}</h1>
            {currentUser && currentUser.is_seaman && (
              <button 
                className="btn btn-primary" 
                onClick={handleApply} 
                disabled={applying}
              >
                {applying ? 'Отправка...' : 'Откликнуться'}
              </button>
            )}
          </div>
          
          <h5 className="card-subtitle mb-3 text-muted">{vacancy.company}</h5>
          
          <div className="row mb-4">
            <div className="col-md-6">
              <div className="mb-2">
                <i className="bi bi-geo-alt me-2"></i>
                <strong>Местоположение:</strong> {vacancy.location}
              </div>
              <div>
                <i className="bi bi-cash me-2"></i>
                <strong>Зарплата:</strong> {vacancy.salary}
              </div>
            </div>
            <div className="col-md-6">
              <div className="mb-2">
                <i className="bi bi-calendar me-2"></i>
                <strong>Опубликовано:</strong> {vacancy.created_at}
              </div>
              <div>
                <i className="bi bi-building me-2"></i>
                <strong>Работодатель:</strong> {vacancy.employer.name}
              </div>
            </div>
          </div>
          
          <hr />
          
          <div className="mb-4">
            <h4>Описание вакансии</h4>
            <p>{vacancy.description}</p>
          </div>
          
          <div className="mb-4">
            <h4>Требования</h4>
            <p>{vacancy.requirements}</p>
          </div>
          
          <div className="mb-4">
            <h4>Обязанности</h4>
            <p>{vacancy.responsibilities}</p>
          </div>
          
          <hr />
          
          <div>
            <h4>Контактная информация</h4>
            <p>
              <i className="bi bi-envelope me-2"></i>
              <a href={`mailto:${vacancy.employer.email}`}>{vacancy.employer.email}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VacancyDetailPage;