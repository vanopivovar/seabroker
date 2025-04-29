import React from 'react';
import { Container, Row, Col, Card, Button, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const { isAuthenticated, currentUser } = useAuth();

  return (
    <>
      {/* Hero Section */}
      <section className="bg-primary text-white py-5 mb-5">
        <Container>
          <Row className="align-items-center">
            <Col md={6} className="mb-4 mb-md-0">
              <h1 className="display-4 fw-bold mb-3">Find Your Sea Career</h1>
              <p className="lead mb-4">
                SeaJobs connects maritime professionals with employers worldwide.
                Find your next opportunity at sea or hire qualified seamen.
              </p>
              <div className="d-flex flex-wrap gap-2">
                {!isAuthenticated ? (
                  <>
                    <Button as={Link} to="/register" variant="light" size="lg">
                      Get Started
                    </Button>
                    <Button as={Link} to="/login" variant="outline-light" size="lg">
                      Sign In
                    </Button>
                  </>
                ) : currentUser?.is_employer ? (
                  <Button as={Link} to="/vacancies/create" variant="light" size="lg">
                    Post a Vacancy
                  </Button>
                ) : (
                  <Button as={Link} to="/vacancies" variant="light" size="lg">
                    Find Jobs
                  </Button>
                )}
              </div>
            </Col>
            <Col md={6}>
              <img 
                src="/images/hero-ship.jpg" 
                alt="Ship at sea" 
                className="img-fluid rounded shadow"
                style={{ opacity: 0.9 }}
              />
            </Col>
          </Row>
        </Container>
      </section>

      {/* Statistics Section */}
      <section className="py-4 mb-5">
        <Container>
          <Row className="text-center">
            <Col md={3} sm={6} className="mb-4">
              <div className="border rounded py-4 h-100">
                <h2 className="display-4 fw-bold text-primary">1,200+</h2>
                <p className="text-muted mb-0">Active Vacancies</p>
              </div>
            </Col>
            <Col md={3} sm={6} className="mb-4">
              <div className="border rounded py-4 h-100">
                <h2 className="display-4 fw-bold text-primary">3,500+</h2>
                <p className="text-muted mb-0">Seamen Resumes</p>
              </div>
            </Col>
            <Col md={3} sm={6} className="mb-4">
              <div className="border rounded py-4 h-100">
                <h2 className="display-4 fw-bold text-primary">450+</h2>
                <p className="text-muted mb-0">Shipping Companies</p>
              </div>
            </Col>
            <Col md={3} sm={6} className="mb-4">
              <div className="border rounded py-4 h-100">
                <h2 className="display-4 fw-bold text-primary">50+</h2>
                <p className="text-muted mb-0">Countries</p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Features Section */}
      <section className="py-5 bg-light mb-5">
        <Container>
          <h2 className="text-center mb-5">How SeaJobs Works</h2>
          <Row>
            <Col md={4} className="mb-4">
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-4" style={{ width: '80px', height: '80px' }}>
                    <i className="bi bi-person-plus-fill fs-1"></i>
                  </div>
                  <Card.Title>Create Your Profile</Card.Title>
                  <Card.Text>
                    Register and create your profile as a seaman or employer. Showcase your skills or company details.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-4" style={{ width: '80px', height: '80px' }}>
                    <i className="bi bi-search fs-1"></i>
                  </div>
                  <Card.Title>Find Opportunities</Card.Title>
                  <Card.Text>
                    Search for maritime jobs or qualified seamen using our advanced filtering system.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-4" style={{ width: '80px', height: '80px' }}>
                    <i className="bi bi-briefcase-fill fs-1"></i>
                  </div>
                  <Card.Title>Apply or Hire</Card.Title>
                  <Card.Text>
                    Apply to vacancies or contact qualified candidates to fill your positions.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Featured Jobs Section */}
      <section className="py-5 mb-5">
        <Container>
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h2>Featured Jobs</h2>
            <Button as={Link} to="/vacancies" variant="outline-primary">
              View All Jobs
            </Button>
          </div>
          <Row>
            {[1, 2, 3].map((job) => (
              <Col md={4} className="mb-4" key={job}>
                <Card className="h-100 shadow-sm hover-shadow">
                  <Card.Body>
                    <div className="d-flex justify-content-between mb-2">
                      <Badge bg="primary">Featured</Badge>
                      <small className="text-muted">Posted 2 days ago</small>
                    </div>
                    <Card.Title>Chief Engineer</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">Global Shipping Co.</Card.Subtitle>
                    <div className="mb-3">
                      <Badge bg="light" text="dark" className="me-2">Container Ship</Badge>
                      <Badge bg="light" text="dark" className="me-2">12 months</Badge>
                      <Badge bg="light" text="dark">$8,000-$10,000</Badge>
                    </div>
                    <Card.Text>
                      Looking for an experienced Chief Engineer for our container vessel.
                      Minimum 5 years experience required.
                    </Card.Text>
                  </Card.Body>
                  <Card.Footer className="bg-white border-top-0">
                    <Button as={Link} to={`/vacancies/${job}`} variant="outline-primary" size="sm">
                      View Details
                    </Button>
                  </Card.Footer>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>
      </section>

      {/* Call-to-Action Sections */}
      <section className="py-5 mb-5">
        <Container>
          <Row>
            <Col md={6} className="mb-4">
              <Card className="bg-primary text-white">
                <Card.Body className="p-4">
                  <h3>For Employers</h3>
                  <p>
                    Find qualified seamen for your vessels. Post job vacancies
                    and connect with maritime professionals around the world.
                  </p>
                  <Button 
                    as={Link} 
                    to={isAuthenticated && currentUser?.is_employer ? "/vacancies/create" : "/register"} 
                    variant="light"
                  >
                    {isAuthenticated && currentUser?.is_employer ? "Post a Vacancy" : "Register as Employer"}
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col md={6} className="mb-4">
              <Card className="bg-secondary text-white">
                <Card.Body className="p-4">
                  <h3>For Seamen</h3>
                  <p>
                    Create your professional profile, upload your resume, and
                    apply to maritime job opportunities worldwide.
                  </p>
                  <Button 
                    as={Link} 
                    to={isAuthenticated && currentUser?.is_seaman ? "/resumes/create" : "/register"} 
                    variant="light"
                  >
                    {isAuthenticated && currentUser?.is_seaman ? "Create Resume" : "Register as Seaman"}
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
    </>
  );
};

export default HomePage;