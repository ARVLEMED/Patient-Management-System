import apiClient from './api';
import { PatientSearch, PatientDetail } from '../types';

export const patientService = {
  // Search patient by national ID
  async searchByNationalId(nationalId: string): Promise<PatientSearch> {
    return await apiClient.get<PatientSearch>('/api/patients/search', { national_id: nationalId });
  },

  // Get patient details (requires consent)
  async getPatientDetails(patientId: string): Promise<PatientDetail> {
    return await apiClient.get<PatientDetail>(`/api/patients/${patientId}`);
  },

  // Get my own profile
  async getMyProfile(): Promise<any> {
    return await apiClient.get<any>('/api/patients/me/profile');
  },

  // Get my full data from registry
  async getMyFullData(): Promise<PatientSearch> {
    return await apiClient.get<PatientSearch>('/api/patients/me/full-data');
  },
};