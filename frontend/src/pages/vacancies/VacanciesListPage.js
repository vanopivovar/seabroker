import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const VacanciesListPage = () => {
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Здесь будет фактический запрос к API за вакансиями
    // Для заглушки используем временные данные
    setTimeout(() => {
      setVacancies([
        { id: 1, title: 'Капитан судна', company: 'Морские линии', location: 'Санкт-Петербург', salary: '200000 руб.' },
        { id: 2, title: 'Бортмеханик', company: 'Северный флот', location: 'Мурманск', salary: '150000 руб.' },
        { id: 3, title: 'Матрос', company: 'Морские перевозки', location: 'Владивосток', salary: '100000 руб.' },
      ]);
      setLoading(false);
    }, 500);
  }, []);
  
  if (loading) {
    return <div className="text-center py-5"><div className="spinner-border"></div></div>;
  }
  
  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }
  
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Вакансии</h1>
        <Link to="/vacancies/create" className="btn btn-primary">Добавить вакансию</Link>
      </div>
      
      <div className="card mb-4">
        <div className="card-body">
          <form>
            <div className="row">
              <div className="col-md-4 mb-2">
                <input type="text" className="form-control" placeholder="Должность или ключевые слова" />
              </div>
              <div className="col-md-3 mb-2">
                <input type="text" className="form-control" placeholder="Город" />
              </div>
              <div className="col-md-3 mb-2">
                <select className="form-select">
                  <option value="">Тип судна</option>
                  <option>Сухогруз</option>
                  <option>Танкер</option>
                  <option>Пассажирское судно</option>
                </select>
              </div>
              <div className="col-md-2 mb-2">
                <button type="submit" className="btn btn-primary w-100">Поиск</button>
              </div>
            </div>
          </form>
        </div>
      </div>
      
      {vacancies.length === 0 ? (
        <div className="alert alert-info">Вакансии не найдены</div>
      ) : (
        <div className="row">
          {vacancies.map(vacancy => (
            <div className="col-md-6 mb-4" key={vacancy.id}>
              <div className="card h-100 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">
                    <Link to={`/vacancies/${vacancy.id}`} className="text-decoration-none">
                      {vacancy.title}
                    </Link>
                  </h5>
                  <h6 className="card-subtitle mb-2 text-muted">{vacancy.company}</h6>
                  <div className="mb-2">
                    <i className="bi bi-geo-alt me-1"></i> {vacancy.location}
                  </div>
                  <div className="mb-3">
                    <i className="bi bi-cash me-1"></i> {vacancy.salary}
                  </div>
                  <Link to={`/vacancies/${vacancy.id}`} className="btn btn-outline-primary">
                    Подробнее
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default VacanciesListPage;