import React from 'react';
import { useParams, Link } from 'react-router-dom';

const ResumeDetailPage = () => {
  const { id } = useParams();
  
  return (
    <div>
      <div className="mb-4">
        <Link to="/resumes" className="btn btn-outline-secondary">
          &larr; Назад к списку резюме
        </Link>
      </div>
      
      <div className="card shadow">
        <div className="card-body">
          <h1 className="card-title mb-3">Детали резюме #{id}</h1>
          <div className="alert alert-info">
            Информация о резюме будет доступна после запуска API
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeDetailPage;