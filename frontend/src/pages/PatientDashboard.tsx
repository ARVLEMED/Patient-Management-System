import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { consentService } from '../services/consentService';
import { facilityService } from '../services/facilityService';
import { accessLogService } from '../services/accessLogService';
import { patientService } from '../services/patientService';
import { Consent, Facility, AccessLog } from '../types';

const PatientDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [consents, setConsents] = useState<Consent[]>([]);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [accessLogs, setAccessLogs] = useState<AccessLog[]>([]);
  const [patientData, setPatientData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Grant consent form state
  const [showGrantForm, setShowGrantForm] = useState(false);
  const [grantForm, setGrantForm] = useState({
    facility_id: '',
    consent_type: 'view' as 'view' | 'edit' | 'share',
    purpose: '',
    expires_at: '',
  });

  const patientId = user?.patient?.patient_id || '';

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Load patient's own data
      const patientProfileData = await patientService.getMyProfile();
      setPatientData(patientProfileData);

      // Load consents
      const consentsData = await consentService.getPatientConsents(patientId);
      setConsents(consentsData.consents);

      // Load facilities
      const facilitiesData = await facilityService.getAllFacilities();
      setFacilities(facilitiesData.facilities);

      // Load access logs
      const logsData = await accessLogService.getPatientAccessLogs(patientId);
      setAccessLogs(logsData.logs);
    } catch (err: any) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGrantConsent = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await consentService.grantConsent({
        ...grantForm,
        expires_at: grantForm.expires_at || undefined,
      });
      
      setSuccess('Consent granted successfully!');
      setShowGrantForm(false);
      setGrantForm({
        facility_id: '',
        consent_type: 'view',
        purpose: '',
        expires_at: '',
      });
      
      // Reload consents
      const consentsData = await consentService.getPatientConsents(patientId);
      setConsents(consentsData.consents);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to grant consent');
    }
  };

  const handleRevokeConsent = async (consentId: string) => {
    if (!window.confirm('Are you sure you want to revoke this consent?')) {
      return;
    }

    setError('');
    setSuccess('');

    try {
      await consentService.revokeConsent(consentId);
      setSuccess('Consent revoked successfully!');
      
      // Reload consents
      const consentsData = await consentService.getPatientConsents(patientId);
      setConsents(consentsData.consents);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to revoke consent');
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

  if (loading) {
    return (
      <div className="dashboard">
        <nav className="navbar">
          <h1>Patient Management System</h1>
        </nav>
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h1>Patient Management System</h1>
        <div className="nav-info">
          <span className="user-info">
            {user?.patient?.first_name} {user?.patient?.last_name} (Patient)
          </span>
          <button onClick={logout} className="btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2>My Dashboard</h2>
          <p>Manage your healthcare consents and view access logs</p>
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
            <h4>Access Logs</h4>
            <div className="stat-value">{accessLogs.length}</div>
          </div>
          <div className="stat-card">
            <h4>Denied Access</h4>
            <div className="stat-value">
              {accessLogs.filter(l => l.result === 'denied').length}
            </div>
          </div>
        </div>

        {/* Grant Consent Section */}
        <div className="card">
          <h3>Grant New Consent</h3>
          
          {!showGrantForm ? (
            <button 
              onClick={() => setShowGrantForm(true)} 
              className="btn btn-success"
            >
              + Grant Consent to Facility
            </button>
          ) : (
            <form onSubmit={handleGrantConsent}>
              <div className="form-group">
                <label>Healthcare Facility</label>
                <select
                  value={grantForm.facility_id}
                  onChange={(e) => setGrantForm({ ...grantForm, facility_id: e.target.value })}
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

              <div className="form-group">
                <label>Consent Type</label>
                <select
                  value={grantForm.consent_type}
                  onChange={(e) => setGrantForm({ ...grantForm, consent_type: e.target.value as any })}
                  required
                >
                  <option value="view">View - Read my medical data</option>
                  <option value="edit">Edit - Read and update my records</option>
                  <option value="share">Share - Read and share with other facilities</option>
                </select>
              </div>

              <div className="form-group">
                <label>Purpose</label>
                <textarea
                  value={grantForm.purpose}
                  onChange={(e) => setGrantForm({ ...grantForm, purpose: e.target.value })}
                  required
                  rows={3}
                  placeholder="Why are you granting this consent?"
                  style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '2px solid #e0e0e0' }}
                />
              </div>

              <div className="form-group">
                <label>Expiration Date (Optional)</label>
                <input
                  type="datetime-local"
                  value={grantForm.expires_at}
                  onChange={(e) => setGrantForm({ ...grantForm, expires_at: e.target.value })}
                />
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button type="submit" className="btn btn-success">
                  Grant Consent
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowGrantForm(false)} 
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>

        {/* My Consents */}
        <div className="card">
          <h3>My Consents ({consents.length})</h3>
          
          {consents.length === 0 ? (
            <div className="empty-state">
              <p>You haven't granted any consents yet.</p>
              <p>Grant consent to allow healthcare facilities to access your data.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Facility</th>
                    <th>Type</th>
                    <th>Purpose</th>
                    <th>Granted</th>
                    <th>Expires</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {consents.map(consent => (
                    <tr key={consent.consent_id}>
                      <td>{consent.facility_name || consent.facility_id}</td>
                      <td>
                        <span className="badge badge-info">
                          {consent.consent_type.toUpperCase()}
                        </span>
                      </td>
                      <td>{consent.purpose.substring(0, 50)}...</td>
                      <td>{new Date(consent.granted_at).toLocaleDateString()}</td>
                      <td>
                        {consent.expires_at 
                          ? new Date(consent.expires_at).toLocaleDateString()
                          : 'Never'}
                      </td>
                      <td>{getStatusBadge(consent.status)}</td>
                      <td>
                        {consent.status === 'active' && (
                          <button
                            onClick={() => handleRevokeConsent(consent.consent_id)}
                            className="btn btn-danger"
                            style={{ padding: '6px 12px', fontSize: '12px' }}
                          >
                            Revoke
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Access Logs */}
        <div className="card">
          <h3>Who Accessed My Data ({accessLogs.length})</h3>
          
          {accessLogs.length === 0 ? (
            <div className="empty-state">
              <p>No access attempts recorded yet.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Date & Time</th>
                    <th>Facility</th>
                    <th>Healthcare Worker</th>
                    <th>Action</th>
                    <th>Result</th>
                    <th>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {accessLogs.map(log => (
                    <tr key={log.log_id}>
                      <td>{new Date(log.timestamp).toLocaleString()}</td>
                      <td>{log.facility_name || log.facility_id}</td>
                      <td>{log.worker_name || log.accessed_by}</td>
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

export default PatientDashboard;