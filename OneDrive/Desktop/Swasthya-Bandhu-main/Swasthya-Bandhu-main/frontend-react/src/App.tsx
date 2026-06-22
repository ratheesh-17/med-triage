import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import DoctorRegistration from './pages/DoctorRegistration'
import PatientDashboard from './pages/patient/Dashboard'
import DoctorDashboard from './pages/doctor/Dashboard'
import AdminDashboard from './pages/admin/Dashboard'
import DoctorSearch from './pages/patient/DoctorSearch'
import AppointmentBooking from './pages/patient/AppointmentBooking'
import Appointments from './pages/patient/Appointments'
import FamilyManagement from './pages/patient/FamilyManagement'
import ProfileSettings from './pages/patient/ProfileSettings'
import HealthReport from './pages/patient/HealthReport'
import SlotManagement from './pages/doctor/SlotManagement'
import PatientHistory from './pages/doctor/PatientHistory'
import AppointmentHistory from './pages/doctor/AppointmentHistory'
import PerformanceAnalytics from './pages/doctor/PerformanceAnalytics'
import DoctorProfile from './pages/doctor/ProfileManagement'
import DoctorVerification from './pages/admin/DoctorVerification'
import PatientManagement from './pages/admin/PatientManagement'
import AppointmentsOverview from './pages/admin/AppointmentsOverview'
import AnalyticsDeepDive from './pages/admin/AnalyticsDeepDive'
import OutbreakDetail from './pages/admin/OutbreakDetail'
import AuditLog from './pages/admin/AuditLog'
import PlatformSettings from './pages/admin/PlatformSettings'
import SystemDebug from './pages/admin/SystemDebug'
import UserManagement from './pages/admin/UserManagement'
import GovernmentReport from './pages/admin/GovernmentReport'
import { authService } from './services/auth'

function ProtectedRoute({ children, allowedRoles }: { children: React.ReactNode; allowedRoles: string[] }) {
  const token = authService.getToken()
  const role = authService.getRole()

  if (!token) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.includes(role || '')) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/doctor/register" element={<DoctorRegistration />} />
          
          <Route
            path="/patient/dashboard"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <PatientDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/doctors"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <DoctorSearch />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/book-appointment/:doctorId"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <AppointmentBooking />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/appointments"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <Appointments />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/family"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <FamilyManagement />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/profile"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <ProfileSettings />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patient/report/:sessionId"
            element={
              <ProtectedRoute allowedRoles={['patient']}>
                <HealthReport />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/dashboard"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <DoctorDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/slots"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <SlotManagement />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/patient-history/:patientId"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <PatientHistory />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/appointments"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <AppointmentHistory />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/analytics"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <PerformanceAnalytics />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/doctor/profile"
            element={
              <ProtectedRoute allowedRoles={['doctor']}>
                <DoctorProfile />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/doctor-verification"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <DoctorVerification />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/patient-management"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <PatientManagement />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/appointments"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AppointmentsOverview />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/analytics"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AnalyticsDeepDive />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/outbreak-detail/:region"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <OutbreakDetail />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/audit-log"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AuditLog />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/settings"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <PlatformSettings />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/debug"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <SystemDebug />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/users"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <UserManagement />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/government-report"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <GovernmentReport />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
