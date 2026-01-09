import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminService } from '../services/accessLogService';
import { SystemStatistics, User, AccessLog } from '../types';

const AdminDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [statistics, setStatistics] = useState<SystemStatistics | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [auditLogs, setAuditLogs] = useState<AccessLog[]>([]);
  const [filterResult, setFilterResult] = useState<'all' | 'allowed' | 'denied'>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [filterResult]);

  const loadData = async () => {
    setLoading(true);
    setError('');

    try {
      // Load statistics
      const stats = await adminService.getStatistics();
      setStatistics(stats);

      // Load users
      const usersData = await adminService.getAllUsers(100);
      setUsers(usersData.users);

      // Load audit logs
      const logsData = await adminService.getAuditLogs(
        100,
        filterResult === 'all' ? undefined : filterResult
      );
      setAuditLogs(logsData.logs);
    } catch (err: any) {
      setError('Failed to load admin data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getResultBadge = (result: string) => {
    return result === 'allowed' ? (
      <span className="badge badge-success">ALLOWED</span>
    ) : (
      <span className="badge badge-danger">DENIED</span>
    );
  };

  const getRoleBadge = (role: string) => {
    const badgeClass = {
      patient: 'badge-info',
      healthcare_worker: 'badge-success',
      admin: 'badge-danger',
    }[role] || 'badge-secondary';
    
    return <span className={`badge ${badgeClass}`}>{role.replace('_', ' ').toUpperCase()}</span>;
  };

  if (loading && !statistics) {
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
          <span className="user-info">{user?.user.email} (Admin)</span>
          <button onClick={logout} className="btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2>Admin Dashboard</h2>
          <p>System overview and audit logs</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        {/* System Statistics */}
        {statistics && (
          <>
            <h3 style={{ marginTop: '20px', marginBottom: '15px' }}>System Statistics</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Total Users</h4>
                <div className="stat-value">{statistics.total_users}</div>
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                  {statistics.total_patients} patients, {statistics.total_healthcare_workers} workers
                </p>
              </div>

              <div className="stat-card">
                <h4>Healthcare Facilities</h4>
                <div className="stat-value">{statistics.total_facilities}</div>
              </div>

              <div className="stat-card">
                <h4>Total Consents</h4>
                <div className="stat-value">{statistics.total_consents}</div>
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                  {statistics.active_consents} active
                </p>
              </div>

              <div className="stat-card">
                <h4>Access Logs</h4>
                <div className="stat-value">{statistics.total_access_logs}</div>
                <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                  {statistics.allowed_access_count} allowed, {statistics.denied_access_count} denied
                </p>
              </div>
            </div>

            <div className="stats-grid" style={{ marginTop: '15px' }}>
              <div className="stat-card">
                <h4>Allowed Access Rate</h4>
                <div className="stat-value" style={{ fontSize: '24px' }}>
                  {statistics.total_access_logs > 0
                    ? Math.round((statistics.allowed_access_count / statistics.total_access_logs) * 100)
                    : 0}%
                </div>
              </div>

              <div className="stat-card">
                <h4>Denied Access Rate</h4>
                <div className="stat-value" style={{ fontSize: '24px' }}>
                  {statistics.total_access_logs > 0
                    ? Math.round((statistics.denied_access_count / statistics.total_access_logs) * 100)
                    : 0}%
                </div>
              </div>

              <div className="stat-card">
                <h4>Consent Approval Rate</h4>
                <div className="stat-value" style={{ fontSize: '24px' }}>
                  {statistics.total_consents > 0
                    ? Math.round((statistics.active_consents / statistics.total_consents) * 100)
                    : 0}%
                </div>
              </div>

              <div className="stat-card">
                <h4>Avg Consents per Patient</h4>
                <div className="stat-value" style={{ fontSize: '24px' }}>
                  {statistics.total_patients > 0
                    ? (statistics.total_consents / statistics.total_patients).toFixed(1)
                    : 0}
                </div>
              </div>
            </div>
          </>
        )}

        {/* All Users */}
        <div className="card">
          <h3>All Users ({users.length})</h3>
          
          {users.length === 0 ? (
            <div className="empty-state">
              <p>No users found.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Last Login</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.user_id}>
                      <td>{user.email}</td>
                      <td>{getRoleBadge(user.role)}</td>
                      <td>
                        {user.is_active ? (
                          <span className="badge badge-success">ACTIVE</span>
                        ) : (
                          <span className="badge badge-danger">INACTIVE</span>
                        )}
                      </td>
                      <td>{new Date(user.created_at).toLocaleDateString()}</td>
                      <td>
                        {user.last_login
                          ? new Date(user.last_login).toLocaleString()
                          : 'Never'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* System Audit Logs */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
            <h3>System Audit Logs ({auditLogs.length})</h3>
            
            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                onClick={() => setFilterResult('all')}
                className={`btn ${filterResult === 'all' ? 'btn-success' : 'btn-secondary'}`}
                style={{ padding: '6px 12px', fontSize: '12px' }}
              >
                All
              </button>
              <button
                onClick={() => setFilterResult('allowed')}
                className={`btn ${filterResult === 'allowed' ? 'btn-success' : 'btn-secondary'}`}
                style={{ padding: '6px 12px', fontSize: '12px' }}
              >
                Allowed
              </button>
              <button
                onClick={() => setFilterResult('denied')}
                className={`btn ${filterResult === 'denied' ? 'btn-success' : 'btn-secondary'}`}
                style={{ padding: '6px 12px', fontSize: '12px' }}
              >
                Denied
              </button>
            </div>
          </div>
          
          {auditLogs.length === 0 ? (
            <div className="empty-state">
              <p>No audit logs found.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Patient</th>
                    <th>Healthcare Worker</th>
                    <th>Facility</th>
                    <th>Action</th>
                    <th>Result</th>
                    <th>Reason</th>
                    <th>IP Address</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map(log => (
                    <tr key={log.log_id}>
                      <td style={{ fontSize: '12px' }}>
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td>
                        {log.patient_name || log.patient_id.substring(0, 10)}
                      </td>
                      <td>
                        {log.worker_name || log.accessed_by.substring(0, 10)}
                      </td>
                      <td>
                        {log.facility_name || log.facility_id.substring(0, 10)}
                      </td>
                      <td>
                        <span className="badge badge-info">
                          {log.action.toUpperCase()}
                        </span>
                      </td>
                      <td>{getResultBadge(log.result)}</td>
                      <td style={{ 
                        color: log.result === 'denied' ? '#d32f2f' : '#666',
                        fontSize: '12px'
                      }}>
                        {log.reason || 'Access granted'}
                      </td>
                      <td style={{ fontSize: '12px' }}>
                        {log.ip_address || 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Security Insights */}
        {statistics && (
          <div className="card">
            <h3>Security Insights</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div>
                <h4>Access Control Effectiveness</h4>
                <p style={{ fontSize: '14px', color: '#666', marginTop: '10px' }}>
                  The system has processed <strong>{statistics.total_access_logs}</strong> access attempts.
                </p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                  <strong>{statistics.denied_access_count}</strong> attempts were denied due to missing or invalid consent, 
                  demonstrating effective access control.
                </p>
              </div>

              <div>
                <h4>Consent Management</h4>
                <p style={{ fontSize: '14px', color: '#666', marginTop: '10px' }}>
                  <strong>{statistics.active_consents}</strong> out of <strong>{statistics.total_consents}</strong> total 
                  consents are currently active.
                </p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                  Each patient has granted an average of <strong>
                  {statistics.total_patients > 0 
                    ? (statistics.total_consents / statistics.total_patients).toFixed(1) 
                    : 0}
                  </strong> consents.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;