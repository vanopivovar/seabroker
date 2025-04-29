import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-dark text-light py-4 mt-auto">
      <Container>
        <Row className="mb-3">
          <Col md={4} className="mb-3 mb-md-0">
            <h5>Sea<strong>Jobs</strong></h5>
            <p className="text-muted small">
              Maritime employment platform connecting seamen and employers worldwide.
            </p>
          </Col>
          
          <Col md={2} className="mb-3 mb-md-0">
            <h6>Company</h6>
            <ul className="list-unstyled">
              <li><Link to="/about" className="text-decoration-none text-muted">About Us</Link></li>
              <li><Link to="/contact" className="text-decoration-none text-muted">Contact</Link></li>
              <li><Link to="/careers" className="text-decoration-none text-muted">Careers</Link></li>
            </ul>
          </Col>
          
          <Col md={2} className="mb-3 mb-md-0">
            <h6>Resources</h6>
            <ul className="list-unstyled">
              <li><Link to="/help" className="text-decoration-none text-muted">Help Center</Link></li>
              <li><Link to="/blog" className="text-decoration-none text-muted">Blog</Link></li>
              <li><Link to="/faq" className="text-decoration-none text-muted">FAQ</Link></li>
            </ul>
          </Col>
          
          <Col md={4}>
            <h6>Connect with us</h6>
            <ul className="list-unstyled d-flex">
              <li className="me-3">
                <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="text-decoration-none text-muted">
                  <i className="bi bi-facebook fs-5"></i>
                </a>
              </li>
              <li className="me-3">
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-decoration-none text-muted">
                  <i className="bi bi-twitter fs-5"></i>
                </a>
              </li>
              <li className="me-3">
                <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-decoration-none text-muted">
                  <i className="bi bi-linkedin fs-5"></i>
                </a>
              </li>
              <li>
                <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-decoration-none text-muted">
                  <i className="bi bi-instagram fs-5"></i>
                </a>
              </li>
            </ul>
          </Col>
        </Row>
        
        <hr className="my-2 border-secondary" />
        
        <Row className="align-items-center">
          <Col md={6} className="text-center text-md-start">
            <p className="mb-0 small text-muted">
              &copy; {currentYear} SeaJobs. All rights reserved.
            </p>
          </Col>
          <Col md={6} className="text-center text-md-end">
            <ul className="list-inline mb-0 small">
              <li className="list-inline-item">
                <Link to="/terms" className="text-decoration-none text-muted">Terms of Service</Link>
              </li>
              <li className="list-inline-item mx-2">&#8226;</li>
              <li className="list-inline-item">
                <Link to="/privacy" className="text-decoration-none text-muted">Privacy Policy</Link>
              </li>
              <li className="list-inline-item mx-2">&#8226;</li>
              <li className="list-inline-item">
                <Link to="/cookies" className="text-decoration-none text-muted">Cookie Policy</Link>
              </li>
            </ul>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;