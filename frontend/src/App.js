import React from 'react';
import { Routes, Route, Navigate, Link } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import NavBar from './components/layout/NavBar';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import PasswordResetPage from './pages/auth/PasswordResetPage';
import ProfilePage from './pages/profile/ProfilePage';
import VacanciesListPage from './pages/vacancies/VacanciesListPage';
import VacancyDetailPage from './pages/vacancies/VacancyDetailPage';
import VacancyCreatePage from './pages/vacancies/VacancyCreatePage';
import ResumesListPage from './pages/resumes/ResumesListPage';
import ResumeDetailPage from './pages/resumes/ResumeDetailPage';
import ResumeCreatePage from './pages/resumes/ResumeCreatePage';
import ApplicationsListPage from './pages/applications/ApplicationsListPage';
import MessagesPage from './pages/messages/MessagesPage';
import NotificationsPage from './pages/notifications/NotificationsPage';
// NotFoundPage component defined inline instead of importing
const NotFoundPage = () => (
  <div className="text-center my-5">
    <h1 className="display-1">404</h1>
    <h2 className="mb-4">Страница не найдена</h2>
    <p className="lead mb-4">Запрашиваемая страница не существует или была перемещена.</p>
    <Link to="/" className="btn btn-primary">
      Вернуться на главную
    </Link>
  </div>
);

// Protected route component
const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Employer only route component
const EmployerRoute = ({ children }) => {
  const { isAuthenticated, currentUser } = useAuth();
  return isAuthenticated && currentUser?.is_employer ? children : <Navigate to="/" />;
};

// Seaman only route component
const SeamanRoute = ({ children }) => {
  const { isAuthenticated, currentUser } = useAuth();
  return isAuthenticated && currentUser?.is_seaman ? children : <Navigate to="/" />;
};

function App() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <NavBar />
      <main className="flex-grow-1 py-4">
        <div className="container">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/password-reset" element={<PasswordResetPage />} />
            <Route path="/password-reset/:uid/:token" element={<PasswordResetPage />} />
            
            {/* Vacancies routes */}
            <Route path="/vacancies" element={<VacanciesListPage />} />
            <Route path="/vacancies/:id" element={<VacancyDetailPage />} />
            <Route path="/vacancies/create" element={
              <EmployerRoute>
                <VacancyCreatePage />
              </EmployerRoute>
            } />
            
            {/* Resumes routes */}
            <Route path="/resumes" element={<ResumesListPage />} />
            <Route path="/resumes/:id" element={<ResumeDetailPage />} />
            <Route path="/resumes/create" element={
              <SeamanRoute>
                <ResumeCreatePage />
              </SeamanRoute>
            } />
            
            {/* Protected routes */}
            <Route path="/profile" element={
              <PrivateRoute>
                <ProfilePage />
              </PrivateRoute>
            } />
            <Route path="/applications" element={
              <PrivateRoute>
                <ApplicationsListPage />
              </PrivateRoute>
            } />
            <Route path="/messages" element={
              <PrivateRoute>
                <MessagesPage />
              </PrivateRoute>
            } />
            <Route path="/notifications" element={
              <PrivateRoute>
                <NotificationsPage />
              </PrivateRoute>
            } />
            
            {/* 404 Page */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;