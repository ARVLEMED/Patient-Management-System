import React, { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface PrivateRouteProps {
  children: ReactNode;
  allowedRoles: string[];
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(user.user.role)) {
    // Redirect to appropriate dashboard based on role
    const dashboardMap: { [key: string]: string } = {
      patient: '/patient',
      healthcare_worker: '/worker',
      admin: '/admin',
    };
    return <Navigate to={dashboardMap[user.user.role] || '/login'} replace />;
  }

  return <>{children}</>;
};

export default PrivateRoute;