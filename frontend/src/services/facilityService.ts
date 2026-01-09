import apiClient from './api';
import { Facility } from '../types';

export const facilityService = {
  // Get all facilities
  async getAllFacilities(): Promise<{ facilities: Facility[], total: number }> {
    return await apiClient.get<{ facilities: Facility[], total: number }>('/api/facilities');
  },

  // Get facility by ID
  async getFacilityById(facilityId: string): Promise<Facility> {
    return await apiClient.get<Facility>(`/api/facilities/${facilityId}`);
  },
};