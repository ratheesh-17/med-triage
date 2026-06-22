export interface User {
  id: number
  phone: string
  name: string
  age: number
  gender: string
  role: 'patient' | 'doctor' | 'admin'
}

export interface Doctor {
  id: number
  phone: string
  name: string
  specialization: string
  hospital: string
  experience: string
  fees: number
  rating: number
  location_lat: number
  location_lng: number
  distance_km?: number
  verification_status: 'pending' | 'approved' | 'rejected'
}

export interface ChatSession {
  id: number
  user_id: number
  symptom_input: string
  severity_score: number
  urgency: string
  recommended_specialist: string
  risk_factors: string[]
  suggested_tests: string[]
  differential_diagnoses: string[]
  clinical_summary: string
  created_at: string
}

export interface Appointment {
  id: number
  user_id: number
  doctor_id: number
  date: string
  time: string
  slot_type: string
  symptom_notes: string
  status: 'confirmed' | 'completed' | 'cancelled'
  doctor?: {
    name: string
    specialization: string
    hospital: string
  }
  patient?: {
    name: string
    age: number
    gender: string
  }
  pre_consult_summary?: {
    severity_score: number
    urgency: string
    risk_factors: string[]
    suggested_tests: string[]
    differential_diagnoses: string[]
  }
}

export interface HealthRisk {
  cardiac: number
  metabolic: number
  neurological: number
  respiratory: number
  overall: number
  trend: string
}

export interface FamilyMember {
  id: number
  name: string
  age: number
  relationship: string
}

export interface AuthResponse {
  token?: string
  role?: string
  user_id?: number
  doctor_id?: number
  otp_sent?: boolean
  message?: string
}
