import React from 'react';
import { Link } from 'react-router-dom';

const ResumesListPage = () => {
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Резюме</h1>
        <Link to="/resumes/create" className="btn btn-primary">Создать резюме</Link>
      </div>
      
      <div className="alert alert-info">
        Список резюме будет доступен после запуска API
      </div>
    </div>
  );
};

export default ResumesListPage;