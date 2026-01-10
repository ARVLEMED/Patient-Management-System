import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { patientService } from '../services/patientService';
import { consentService } from '../services/consentService';
import { accessLogService } from '../services/accessLogService';
import { PatientSearch, PatientDetail, Consent, AccessLog } from '../types';

const WorkerDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [searchNationalId, setSearchNationalId] = useState('');
  const [searchResult, setSearchResult] = useState<PatientSearch | null>(null);
  const [patientDetail, setPatientDetail] = useState<PatientDetail | null>(null);
  const [consents, setConsents] = useState<Consent[]>([]);
  const [accessLogs, setAccessLogs] = useState<AccessLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const facilityId = user?.healthcare_worker?.facility_id || '';

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      // Load facility's consents
      if (facilityId) {
        const consentsData = await consentService.getFacilityConsents(facilityId);
        setConsents(consentsData.consents);
      }

      // Load my access logs
      const logsData = await accessLogService.getMyWorkerAccessLogs();
      setAccessLogs(logsData.logs);
    } catch (err) {
      console.error('Failed to load initial data', err);
    }
  };

  const handleSearchPatient = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSearchResult(null);
    setPatientDetail(null);
    setLoading(true);

    try {
      const result = await patientService.searchByNationalId(searchNationalId);
      setSearchResult(result);
      setSuccess(`Patient found: ${result.first_name} ${result.last_name}`);
    } catch (err: any) {
      console.error('Search error:', err);
      
      const detail = err.response?.data?.detail;
      
      if (err.response?.status === 404) {
        setError('Patient not found in central registry');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        const messages = detail.map((d: any) => 
          typeof d === 'string' ? d : (d.msg || JSON.stringify(d))
        );
        setError(messages.join(', '));
      } else {
        setError('Failed to search patient. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleViewPatientData = async (patientId: string) => {
    setError('');
    setSuccess('');
    setPatientDetail(null);
    setLoading(true);

    try {
      const detail = await patientService.getPatientDetails(patientId);
      setPatientDetail(detail);
      setSuccess('Patient data accessed successfully');
      
      // Reload access logs
      const logsData = await accessLogService.getMyWorkerAccessLogs();
      setAccessLogs(logsData.logs);
    } catch (err: any) {
      console.error('Access patient data error:', err);
      
      const detail = err.response?.data?.detail;
      
      if (err.response?.status === 403) {
        // Access denied - show clear message
        const message = typeof detail === 'string' ? detail : 'Access denied: No valid consent found';
        setError(message);
      } else if (err.response?.status === 404) {
        setError('Patient not found in local system. Patient must register first.');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        const messages = detail.map((d: any) => 
          typeof d === 'string' ? d : (d.msg || JSON.stringify(d))
        );
        setError(messages.join(', '));
      } else {
        setError('Failed to access patient data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const badgeClass = {
      active: 'badge-success',
      expired: 'badge-warning',
      revoked: 'badge-danger',
    }[status] || 'badge-secondary';
    
    return <span className={`badge ${badgeClass}`}>{status.toUpperCase()}</span>;
  };

  const getResultBadge = (result: string) => {
    return result === 'allowed' ? (
      <span className="badge badge-success">ALLOWED</span>
    ) : (
      <span className="badge badge-danger">DENIED</span>
    );
  };

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h1>Patient Management System</h1>
        <div className="nav-info">
          <span className="user-info">
            {user?.healthcare_worker?.job_title} at {user?.healthcare_worker?.facility_name}
          </span>
          <button onClick={logout} className="btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2>Healthcare Worker Dashboard</h2>
          <p>Search and access patient data with proper consent</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Statistics */}
        <div className="stats-grid">
          <div className="stat-card">
            <h4>Active Consents</h4>
            <div className="stat-value">
              {consents.filter(c => c.status === 'active').length}
            </div>
          </div>
          <div className="stat-card">
            <h4>Total Consents</h4>
            <div className="stat-value">{consents.length}</div>
          </div>
          <div className="stat-card">
            <h4>My Access Logs</h4>
            <div className="stat-value">{accessLogs.length}</div>
          </div>
          <div className="stat-card">
            <h4>Denied Access</h4>
            <div className="stat-value">
              {accessLogs.filter(l => l.result === 'denied').length}
            </div>
          </div>
        </div>

        {/* Search Patient */}
        <div className="card">
          <h3>Search Patient by National ID</h3>
          
          <form onSubmit={handleSearchPatient}>
            <div className="form-inline">
              <div className="form-group">
                <label>National ID</label>
                <input
                  type="text"
                  value={searchNationalId}
                  onChange={(e) => setSearchNationalId(e.target.value)}
                  placeholder="Enter patient's National ID (e.g., 12345678)"
                  required
                />
              </div>
              <button type="submit" className="btn btn-success" disabled={loading}>
                {loading ? 'Searching...' : 'Search Patient'}
              </button>
            </div>
          </form>

          {searchResult && (
            <div style={{ marginTop: '20px', padding: '15px', background: '#f5f5f5', borderRadius: '5px' }}>
              <h4>Patient Found in Registry</h4>
              <p><strong>Name:</strong> {searchResult.first_name} {searchResult.last_name}</p>
              <p><strong>Patient ID:</strong> {searchResult.patient_id}</p>
              <p><strong>Gender:</strong> {searchResult.gender}</p>
              <p><strong>Date of Birth:</strong> {searchResult.date_of_birth}</p>
              <p><strong>Location:</strong> {searchResult.address.county}, {searchResult.address.sub_county}</p>
              
              <button
                onClick={() => handleViewPatientData(searchResult.patient_id)}
                className="btn btn-success"
                style={{ marginTop: '10px' }}
                disabled={loading}
              >
                {loading ? 'Accessing...' : 'Access Full Patient Data (Requires Consent)'}
              </button>
            </div>
          )}
        </div>

        {/* Patient Detail View */}
        {patientDetail && (
          <div className="card">
            <h3>Patient Details</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div>
                <h4>Personal Information</h4>
                <p><strong>Name:</strong> {patientDetail.first_name} {patientDetail.last_name}</p>
                <p><strong>Patient ID:</strong> {patientDetail.patient_id}</p>
                <p><strong>National ID:</strong> {patientDetail.national_id}</p>
                <p><strong>Gender:</strong> {patientDetail.gender}</p>
                <p><strong>Date of Birth:</strong> {patientDetail.date_of_birth}</p>
                <p><strong>Phone:</strong> {patientDetail.phone}</p>
                <p><strong>Email:</strong> {patientDetail.email}</p>
              </div>

              <div>
                <h4>Address</h4>
                <p><strong>County:</strong> {patientDetail.address.county}</p>
                <p><strong>Sub-County:</strong> {patientDetail.address.sub_county}</p>
                <p><strong>Ward:</strong> {patientDetail.address.ward}</p>
                
                <h4 style={{ marginTop: '20px' }}>Emergency Contact</h4>
                <p><strong>Name:</strong> {patientDetail.emergency_contact.name}</p>
                <p><strong>Relationship:</strong> {patientDetail.emergency_contact.relationship}</p>
                <p><strong>Phone:</strong> {patientDetail.emergency_contact.phone}</p>
              </div>
            </div>

            <div style={{ marginTop: '20px', padding: '10px', background: '#e3f2fd', borderRadius: '5px' }}>
              <p><strong>Consent Type:</strong> <span className="badge badge-info">{patientDetail.consent_type.toUpperCase()}</span></p>
              <p><strong>Access Granted At:</strong> {new Date(patientDetail.access_granted_at).toLocaleString()}</p>
            </div>
          </div>
        )}

        {/* Consented Patients */}
        <div className="card">
          <h3>Patients with Active Consent ({consents.filter(c => c.status === 'active').length})</h3>
          
          {consents.filter(c => c.status === 'active').length === 0 ? (
            <div className="empty-state">
              <p>No patients have granted consent to your facility yet.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Patient ID</th>
                    <th>Consent Type</th>
                    <th>Purpose</th>
                    <th>Granted</th>
                    <th>Expires</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {consents.filter(c => c.status === 'active').map(consent => (
                    <tr key={consent.consent_id}>
                      <td>{consent.patient_id}</td>
                      <td>
                        <span className="badge badge-info">
                          {consent.consent_type.toUpperCase()}
                        </span>
                      </td>
                      <td>{consent.purpose.substring(0, 40)}...</td>
                      <td>{new Date(consent.granted_at).toLocaleDateString()}</td>
                      <td>
                        {consent.expires_at 
                          ? new Date(consent.expires_at).toLocaleDateString()
                          : 'Never'}
                      </td>
                      <td>
                        <button
                          onClick={() => handleViewPatientData(consent.patient_id)}
                          className="btn btn-success"
                          style={{ padding: '6px 12px', fontSize: '12px' }}
                          disabled={loading}
                        >
                          View Data
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* My Access Logs */}
        <div className="card">
          <h3>My Access Log History ({accessLogs.length})</h3>
          
          {accessLogs.length === 0 ? (
            <div className="empty-state">
              <p>You haven't accessed any patient data yet.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Date & Time</th>
                    <th>Patient ID</th>
                    <th>Patient Name</th>
                    <th>Action</th>
                    <th>Result</th>
                    <th>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {accessLogs.slice(0, 20).map(log => (
                    <tr key={log.log_id}>
                      <td>{new Date(log.timestamp).toLocaleString()}</td>
                      <td>{log.patient_id}</td>
                      <td>{log.patient_name || 'N/A'}</td>
                      <td>
                        <span className="badge badge-info">
                          {log.action.toUpperCase()}
                        </span>
                      </td>
                      <td>{getResultBadge(log.result)}</td>
                      <td style={{ color: log.result === 'denied' ? '#d32f2f' : '#666' }}>
                        {log.reason || 'Access granted'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WorkerDashboard;