import api from './api'
import { AuthResponse } from '@/types'

export const authService = {
  registerPatient: async (data: {
    phone: string
    name: string
    age: number
    gender: string
  }): Promise<AuthResponse> => {
    const response = await api.post('/auth/patient/register', data)
    return response.data
  },

  registerDoctor: async (data: {
    phone: string
    name: string
    specialization: string
    hospital: string
    experience: string
    fees: number
    location_lat: number
    location_lng: number
    medical_council_number: string
  }): Promise<{ message: string; status: string }> => {
    const response = await api.post('/auth/doctor/register', data)
    return response.data
  },

  login: async (phone: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', { phone })
    return response.data
  },

  verifyAdminOTP: async (phone: string, otp: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/admin/verify-otp', { phone, otp })
    return response.data
  },

  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
  },

  getToken: () => localStorage.getItem('token'),
  getRole: () => localStorage.getItem('role'),
  
  setAuth: (token: string, role: string) => {
    localStorage.setItem('token', token)
    localStorage.setItem('role', role)
  },
}
