import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      const dashboardMap: { [key: string]: string } = {
        patient: '/patient',
        healthcare_worker: '/worker',
        admin: '/admin',
      };
      navigate(dashboardMap[user.user.role]);
    }
  }, [user, navigate]);

  const features = [
    {
      icon: '🔒',
      title: 'Consent-Based Access',
      description: 'Patients control who can access their medical data with explicit consent management'
    },
    {
      icon: '🏥',
      title: 'Integrated Registry',
      description: 'Seamless integration with Kenya\'s Central Patient Registry for unified healthcare'
    },
    {
      icon: '📊',
      title: 'Audit Logging',
      description: 'Complete transparency with detailed logs of all data access attempts'
    },
    {
      icon: '⚡',
      title: 'Real-Time Security',
      description: 'Advanced encryption and JWT authentication for maximum data protection'
    },
    {
      icon: '🚀',
      title: 'Fast & Reliable',
      description: 'Built with modern technology stack for blazing fast performance'
    },
    {
      icon: '👥',
      title: 'Role-Based Access',
      description: 'Different dashboards for patients, healthcare workers, and administrators'
    }
  ];

  const stats = [
    { number: '15+', label: 'Active Users' },
    { number: '3', label: 'Healthcare Facilities' },
    { number: '100%', label: 'Secure' },
    { number: '24/7', label: 'Available' }
  ];

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero" style={{ transform: `translateY(${scrollY * 0.5}px)` }}>
        <div className="hero-overlay"></div>
        <nav className="navbar-landing">
          <div className="logo">
            <span className="logo-icon">🏥</span>
            <span className="logo-text">HealthHub</span>
          </div>
          <div className="nav-buttons">
            <button onClick={() => navigate('/login')} className="btn-nav">
              Login
            </button>
            <button onClick={() => navigate('/register')} className="btn-nav btn-nav-primary">
              Get Started
            </button>
          </div>
        </nav>

        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            Secure Healthcare Management
          </div>
          <h1 className="hero-title">
            Your Health Data,
            <br />
            <span className="gradient-text">Your Control</span>
          </h1>
          <p className="hero-description">
            A revolutionary patient management system with consent-based access control.
            Empowering patients and healthcare providers with secure, transparent data management.
          </p>
          <div className="hero-buttons">
            <button onClick={() => navigate('/register')} className="btn-hero btn-hero-primary">
              Start Free Trial
              <span className="btn-icon">→</span>
            </button>
            <button onClick={() => navigate('/login')} className="btn-hero btn-hero-secondary">
              <span className="btn-icon">▶</span>
              Watch Demo
            </button>
          </div>

          {/* Floating Cards */}
          <div className="floating-cards">
            <div className="float-card card-1">
              <div className="card-icon">✓</div>
              <div className="card-text">
                <div className="card-title">100% Secure</div>
                <div className="card-desc">End-to-end encryption</div>
              </div>
            </div>
            <div className="float-card card-2">
              <div className="card-icon">⚡</div>
              <div className="card-text">
                <div className="card-title">Lightning Fast</div>
                <div className="card-desc">Sub-second response</div>
              </div>
            </div>
            <div className="float-card card-3">
              <div className="card-icon">🎯</div>
              <div className="card-text">
                <div className="card-title">HIPAA Compliant</div>
                <div className="card-desc">Healthcare standards</div>
              </div>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="scroll-indicator">
          <div className="scroll-line"></div>
          <span>Scroll to explore</span>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          {stats.map((stat, index) => (
            <div key={index} className="stat-item" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="stat-number">{stat.number}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <span className="section-badge">Features</span>
          <h2 className="section-title">Everything You Need for Modern Healthcare</h2>
          <p className="section-description">
            Powerful features designed to give patients control and healthcare providers the tools they need
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => (
            <div 
              key={index} 
              className="feature-card"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <div className="section-header">
          <span className="section-badge">Process</span>
          <h2 className="section-title">How It Works</h2>
        </div>

        <div className="steps-container">
          <div className="step">
            <div className="step-number">01</div>
            <div className="step-content">
              <h3>Register Your Account</h3>
              <p>Choose your role - Patient, Healthcare Worker, or Administrator</p>
            </div>
          </div>

          <div className="step-connector"></div>

          <div className="step">
            <div className="step-number">02</div>
            <div className="step-content">
              <h3>Grant Consent</h3>
              <p>Patients grant explicit consent to healthcare facilities for data access</p>
            </div>
          </div>

          <div className="step-connector"></div>

          <div className="step">
            <div className="step-number">03</div>
            <div className="step-content">
              <h3>Secure Access</h3>
              <p>Healthcare providers access data only with valid consent - all logged</p>
            </div>
          </div>
        </div>
      </section>

      {/* User Types Section */}
      <section className="user-types">
        <div className="section-header">
          <span className="section-badge">Who We Serve</span>
          <h2 className="section-title">Built for Everyone in Healthcare</h2>
        </div>

        <div className="user-cards">
          <div className="user-card user-card-patient">
            <div className="user-icon">👤</div>
            <h3>Patients</h3>
            <ul>
              <li>✓ Control who accesses your data</li>
              <li>✓ View complete access history</li>
              <li>✓ Revoke consent anytime</li>
              <li>✓ Secure medical records</li>
            </ul>
            <button onClick={() => navigate('/register')} className="btn-user">
              Register as Patient
            </button>
          </div>

          <div className="user-card user-card-worker">
            <div className="user-icon">⚕️</div>
            <h3>Healthcare Workers</h3>
            <ul>
              <li>✓ Access patient data securely</li>
              <li>✓ Real-time consent validation</li>
              <li>✓ Integrated registry search</li>
              <li>✓ Comprehensive audit trails</li>
            </ul>
            <button onClick={() => navigate('/register')} className="btn-user">
              Register as Provider
            </button>
          </div>

          <div className="user-card user-card-admin">
            <div className="user-icon">👨‍💼</div>
            <h3>Administrators</h3>
            <ul>
              <li>✓ System-wide analytics</li>
              <li>✓ Complete audit logs</li>
              <li>✓ User management</li>
              <li>✓ Security monitoring</li>
            </ul>
            <button onClick={() => navigate('/register')} className="btn-user">
              Register as Admin
            </button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Transform Healthcare Management?</h2>
          <p>Join thousands of healthcare providers and patients using our secure platform</p>
          <div className="cta-buttons">
            <button onClick={() => navigate('/register')} className="btn-cta btn-cta-primary">
              Get Started Free
            </button>
            <button onClick={() => navigate('/login')} className="btn-cta btn-cta-secondary">
              Sign In
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>HealthHub</h4>
            <p>Secure patient management with consent-based access control</p>
          </div>
          <div className="footer-section">
            <h4>Product</h4>
            <ul>
              <li><a href="#features">Features</a></li>
              <li><a href="#security">Security</a></li>
              <li><a href="#pricing">Pricing</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Resources</h4>
            <ul>
              <li><a href="#docs">Documentation</a></li>
              <li><a href="#api">API Reference</a></li>
              <li><a href="#support">Support</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
              <li><a href="#privacy">Privacy</a></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2026 HealthHub. Built for healthcare innovation.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;