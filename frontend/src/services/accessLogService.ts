import apiClient from './api';
import { AccessLog, SystemStatistics, User } from '../types';

export const accessLogService = {
  // Get patient's access logs
  async getPatientAccessLogs(patientId: string, limit = 100): Promise<{ logs: AccessLog[], total: number }> {
    return await apiClient.get<{ logs: AccessLog[], total: number }>(
      `/api/access-logs/patient/${patientId}`,
      { limit }
    );
  },

  // Get my worker access logs
  async getMyWorkerAccessLogs(limit = 100): Promise<{ logs: AccessLog[], total: number }> {
    return await apiClient.get<{ logs: AccessLog[], total: number }>(
      '/api/access-logs/worker/me',
      { limit }
    );
  },

  // Get facility access logs
  async getFacilityAccessLogs(facilityId: string, limit = 100): Promise<{ logs: AccessLog[], total: number }> {
    return await apiClient.get<{ logs: AccessLog[], total: number }>(
      `/api/access-logs/facility/${facilityId}`,
      { limit }
    );
  },
};

export const adminService = {
  // Get all users
  async getAllUsers(limit = 100, offset = 0): Promise<{ users: User[], total: number }> {
    return await apiClient.get<{ users: User[], total: number }>(
      '/api/admin/users',
      { limit, offset }
    );
  },

  // Get audit logs
  async getAuditLogs(limit = 100, result?: string): Promise<{ logs: AccessLog[], total: number }> {
    const params = result ? { limit, result } : { limit };
    return await apiClient.get<{ logs: AccessLog[], total: number }>(
      '/api/admin/audit-logs',
      params
    );
  },

  // Get system statistics
  async getStatistics(): Promise<SystemStatistics> {
    return await apiClient.get<SystemStatistics>('/api/admin/statistics');
  },
};