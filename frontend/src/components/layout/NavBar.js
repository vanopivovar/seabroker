import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container, Button, Dropdown } from 'react-bootstrap';
import { useAuth } from '../../contexts/AuthContext';

const NavBar = () => {
  const { isAuthenticated, currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const closeMenu = () => setExpanded(false);

  return (
    <Navbar bg="white" expand="lg" className="border-bottom shadow-sm py-2" expanded={expanded}>
      <Container>
        {/* Logo and brand */}
        <Navbar.Brand as={Link} to="/" className="d-flex align-items-center">
          <img
            src="/logo192.png"
            width="30"
            height="30"
            className="d-inline-block align-top me-2"
            alt="SeaJobs Logo"
          />
          <span>Sea<strong>Jobs</strong></span>
        </Navbar.Brand>
        
        <Navbar.Toggle 
          aria-controls="navbar-nav" 
          onClick={() => setExpanded(!expanded)}
        />
        
        <Navbar.Collapse id="navbar-nav">
          {/* Main navigation links */}
          <Nav className="me-auto">
            <Nav.Link as={NavLink} to="/" onClick={closeMenu}>Home</Nav.Link>
            <Nav.Link as={NavLink} to="/vacancies" onClick={closeMenu}>Vacancies</Nav.Link>
            <Nav.Link as={NavLink} to="/resumes" onClick={closeMenu}>Resumes</Nav.Link>
          </Nav>
          
          {/* Authentication links */}
          <Nav>
            {isAuthenticated ? (
              <>
                {/* Links for authenticated users */}
                <Nav.Link as={NavLink} to="/applications" onClick={closeMenu}>Applications</Nav.Link>
                <Nav.Link as={NavLink} to="/messages" onClick={closeMenu}>Messages</Nav.Link>
                
                {/* User dropdown menu */}
                <Dropdown align="end">
                  <Dropdown.Toggle variant="link" id="dropdown-user" className="nav-link">
                    {currentUser?.first_name || currentUser?.email || 'Account'}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    <Dropdown.Item as={Link} to="/profile" onClick={closeMenu}>My Profile</Dropdown.Item>
                    <Dropdown.Item as={Link} to="/notifications" onClick={closeMenu}>Notifications</Dropdown.Item>
                    
                    {/* Employer-specific links */}
                    {currentUser?.is_employer && (
                      <>
                        <Dropdown.Divider />
                        <Dropdown.Item as={Link} to="/vacancies/create" onClick={closeMenu}>Post a Vacancy</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications?received=true" onClick={closeMenu}>
                          Received Applications
                        </Dropdown.Item>
                      </>
                    )}
                    
                    {/* Seaman-specific links */}
                    {currentUser?.is_seaman && (
                      <>
                        <Dropdown.Divider />
                        <Dropdown.Item as={Link} to="/resumes/create" onClick={closeMenu}>Create Resume</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications?my=true" onClick={closeMenu}>
                          My Applications
                        </Dropdown.Item>
                      </>
                    )}
                    
                    <Dropdown.Divider />
                    <Dropdown.Item onClick={() => { closeMenu(); handleLogout(); }}>Logout</Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </>
            ) : (
              <>
                {/* Links for non-authenticated users */}
                <Nav.Item>
                  <Button
                    as={Link}
                    to="/login"
                    variant="outline-primary"
                    className="me-2"
                    onClick={closeMenu}
                  >
                    Login
                  </Button>
                </Nav.Item>
                <Nav.Item>
                  <Button
                    as={Link}
                    to="/register"
                    variant="primary"
                    onClick={closeMenu}
                  >
                    Register
                  </Button>
                </Nav.Item>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;