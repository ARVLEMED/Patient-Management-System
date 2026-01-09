import apiClient from './api';
import { Consent, ConsentCreateRequest } from '../types';

export const consentService = {
  // Grant new consent
  async grantConsent(data: ConsentCreateRequest): Promise<Consent> {
    return await apiClient.post<Consent>('/api/consents', data);
  },

  // Get patient's consents
  async getPatientConsents(patientId: string, status?: string): Promise<{ consents: Consent[], total: number }> {
    const params = status ? { status } : undefined;
    return await apiClient.get<{ consents: Consent[], total: number }>(
      `/api/consents/patient/${patientId}`,
      params
    );
  },

  // Revoke consent
  async revokeConsent(consentId: string): Promise<{ consent_id: string, revoked_at: string, message: string }> {
    return await apiClient.patch<{ consent_id: string, revoked_at: string, message: string }>(
      `/api/consents/${consentId}/revoke`
    );
  },

  // Get facility consents
  async getFacilityConsents(facilityId: string, status?: string): Promise<{ consents: Consent[], total: number }> {
    const params = status ? { status } : undefined;
    return await apiClient.get<{ consents: Consent[], total: number }>(
      `/api/consents/facility/${facilityId}`,
      params
    );
  },
};