import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { facilityService } from '../services/facilityService';
import { Facility } from '../types';
import './Auth.css';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'patient' as 'patient' | 'healthcare_worker' | 'admin',
    first_name: '',
    last_name: '',
    national_id: '',
    date_of_birth: '',
    facility_id: '',
    license_number: '',
    job_title: '',
  });
  
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  // Load facilities for healthcare worker registration
  useEffect(() => {
    if (formData.role === 'healthcare_worker') {
      facilityService.getAllFacilities()
        .then(response => setFacilities(response.facilities))
        .catch(err => console.error('Failed to load facilities', err));
    }
  }, [formData.role]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate role-specific fields
    if (formData.role === 'patient') {
      if (!formData.first_name || !formData.last_name || !formData.national_id || !formData.date_of_birth) {
        setError('Please fill in all patient information');
        return;
      }
    } else if (formData.role === 'healthcare_worker') {
      if (!formData.facility_id || !formData.license_number || !formData.job_title) {
        setError('Please fill in all healthcare worker information');
        return;
      }
    }

    setLoading(true);

    try {
      const { confirmPassword, ...registerData } = formData;
      // For non-patients, remove patient fields
if (formData.role !== 'patient') {
  delete (registerData as any).first_name;
  delete (registerData as any).last_name;
  delete (registerData as any).national_id;
  delete (registerData as any).date_of_birth;
}

// For non-healthcare_worker, remove those fields if desired
if (formData.role !== 'healthcare_worker') {
  delete (registerData as any).facility_id;
  delete (registerData as any).license_number;
  delete (registerData as any).job_title;
}
      await register(registerData);
      // Navigate to appropriate dashboard
      const dashboardMap = {
        patient: '/patient',
        healthcare_worker: '/worker',
        admin: '/admin',
      };
      navigate(dashboardMap[formData.role]);
    } catch (err: any) {
  console.error('Registration error:', err);

  const detail = err.response?.data?.detail;

  if (!detail) {
    setError('Registration failed. Please try again.');
    return;
  }

  // If detail is a string (custom HTTPException)
  if (typeof detail === 'string') {
    setError(detail);
    return;
  }

  // If detail is an array (Pydantic validation errors)
  if (Array.isArray(detail)) {
    const messages = detail.map(d => {
      if (typeof d === 'string') return d;
      if (d.msg) return `${d.loc.join('.')} : ${d.msg}`;
      return JSON.stringify(d);
    });
    setError(messages.join(', '));
    return;
  }

  // If detail is an object
  if (typeof detail === 'object') {
    setError(detail.msg || JSON.stringify(detail));
    return;
  }

  // fallback
  setError('Registration failed. Please try again.');
}


  };

  return (
    <div className="auth-container">
      <div className="auth-box register-box">
        <h1>Patient Management System</h1>
        <h2>Register</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {/* Role Selection */}
          <div className="form-group">
            <label htmlFor="role">I am a:</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
            >
              <option value="patient">Patient</option>
              <option value="healthcare_worker">Healthcare Worker</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          {/* Common Fields */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                minLength={8}
                placeholder="Min 8 characters"
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                placeholder="Re-enter password"
              />
            </div>
          </div>

          {/* Patient-specific fields */}
          {formData.role === 'patient' && (
            <>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="first_name">First Name</label>
                  <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="last_name">Last Name</label>
                  <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="national_id">National ID</label>
                  <input
                    type="text"
                    id="national_id"
                    name="national_id"
                    value={formData.national_id}
                    onChange={handleChange}
                    required
                    placeholder="12345678"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="date_of_birth">Date of Birth</label>
                  <input
                    type="date"
                    id="date_of_birth"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
            </>
          )}

          {/* Healthcare Worker-specific fields */}
          {formData.role === 'healthcare_worker' && (
            <>
              <div className="form-group">
                <label htmlFor="facility_id">Healthcare Facility</label>
                <select
                  id="facility_id"
                  name="facility_id"
                  value={formData.facility_id}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Facility</option>
                  {facilities.map(facility => (
                    <option key={facility.facility_id} value={facility.facility_id}>
                      {facility.name} ({facility.facility_type})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="license_number">License Number</label>
                  <input
                    type="text"
                    id="license_number"
                    name="license_number"
                    value={formData.license_number}
                    onChange={handleChange}
                    required
                    placeholder="MD-12345"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="job_title">Job Title</label>
                  <input
                    type="text"
                    id="job_title"
                    name="job_title"
                    value={formData.job_title}
                    onChange={handleChange}
                    required
                    placeholder="General Practitioner"
                  />
                </div>
              </div>
            </>
          )}

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <div className="auth-links">
          <Link to="/login">Already have an account? Login</Link>
        </div>
      </div>
    </div>
  );
};

export default Register;