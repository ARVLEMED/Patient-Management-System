// User Types
export type UserRole = 'patient' | 'healthcare_worker' | 'admin';

export interface User {
  user_id: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  role: UserRole;
  first_name?: string;
  last_name?: string;
  national_id?: string;
  date_of_birth?: string;
  facility_id?: string;
  license_number?: string;
  job_title?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserProfile {
  user: User;
  patient?: PatientProfile;
  healthcare_worker?: HealthcareWorkerProfile;
}

export interface PatientProfile {
  patient_id: string;
  user_id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  email: string;
  created_at: string;
}

export interface HealthcareWorkerProfile {
  worker_id: string;
  user_id: string;
  facility_id: string;
  facility_name?: string;
  license_number: string;
  job_title: string;
  email: string;
  created_at: string;
}

// Facility Types
export type FacilityType = 'hospital' | 'clinic' | 'pharmacy';

export interface Facility {
  facility_id: string;
  name: string;
  facility_type: FacilityType;
  license_number: string;
  location: string;
  created_at: string;
}

// Consent Types
export type ConsentType = 'view' | 'edit' | 'share';
export type ConsentStatus = 'active' | 'expired' | 'revoked';

export interface Consent {
  consent_id: string;
  patient_id: string;
  facility_id: string;
  facility_name?: string;
  consent_type: ConsentType;
  granted_at: string;
  expires_at?: string;
  revoked_at?: string;
  purpose: string;
  status: ConsentStatus;
}

export interface ConsentCreateRequest {
  facility_id: string;
  consent_type: ConsentType;
  purpose: string;
  expires_at?: string;
}

// Patient Types
export interface PatientSearch {
  patient_id: string;
  national_id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone: string;
  email: string;
  address: {
    county: string;
    sub_county: string;
    ward: string;
  };
  emergency_contact: {
    name: string;
    relationship: string;
    phone: string;
  };
}

export interface PatientDetail extends PatientSearch {
  access_granted_at: string;
  consent_type: string;
}

// Access Log Types
export type AccessResult = 'allowed' | 'denied';

export interface AccessLog {
  log_id: string;
  patient_id: string;
  patient_name?: string;
  accessed_by: string;
  worker_name?: string;
  facility_id: string;
  facility_name?: string;
  action: string;
  result: AccessResult;
  reason?: string;
  timestamp: string;
  ip_address?: string;
}

// Statistics Types
export interface SystemStatistics {
  total_users: number;
  total_patients: number;
  total_healthcare_workers: number;
  total_facilities: number;
  total_consents: number;
  active_consents: number;
  total_access_logs: number;
  allowed_access_count: number;
  denied_access_count: number;
}