import React from 'react';
import { Link } from 'react-router-dom';

const ResumeCreatePage = () => {
  return (
    <div>
      <h1 className="mb-4">Создание резюме</h1>
      
      <div className="card shadow">
        <div className="card-body">
          <div className="alert alert-info">
            Форма создания резюме будет доступна после запуска API
          </div>
          
          <div className="mt-3">
            <Link to="/resumes" className="btn btn-outline-secondary">
              Вернуться к списку резюме
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeCreatePage;