import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Activity, User } from 'lucide-react'
import { authService } from '../../services/auth'
import toast from 'react-hot-toast'
import { Layout, Menu, Avatar, Dropdown, Space } from 'antd'

const { Header } = Layout

export default function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  const token = authService.getToken()
  const role = authService.getRole()

  // Hide navbar on public pages
  const publicPages = ['/', '/login', '/register', '/doctor/register']
  if (publicPages.includes(location.pathname)) {
    return null
  }

  // Only show navbar if user is logged in
  if (!token) {
    return null
  }

  const handleLogout = () => {
    authService.logout()
    toast.success('Logged out successfully')
    navigate('/login')
    window.location.reload()
  }

  const navLinks = role === 'patient'
    ? [
        { label: 'Dashboard', key: '/patient/dashboard', path: '/patient/dashboard' },
        { label: 'Find Doctors', key: '/patient/doctors', path: '/patient/doctors' },
        { label: 'Appointments', key: '/patient/appointments', path: '/patient/appointments' },
        { label: 'Family', key: '/patient/family', path: '/patient/family' }
      ]
    : role === 'doctor'
    ? [
        { label: 'Dashboard', key: '/doctor/dashboard', path: '/doctor/dashboard' },
        { label: 'Manage Schedule', key: '/doctor/slots', path: '/doctor/slots' },
        { label: 'My Appointments', key: '/doctor/appointments', path: '/doctor/appointments' },
        { label: 'My Analytics', key: '/doctor/analytics', path: '/doctor/analytics' }
      ]
    : [
        { label: 'Dashboard', key: '/admin/dashboard', path: '/admin/dashboard' },
        { label: 'Doctor Verification', key: '/admin/doctor-verification', path: '/admin/doctor-verification' },
        { label: 'User Management', key: '/admin/users', path: '/admin/users' },
        { label: 'Government Report', key: '/admin/government-report', path: '/admin/government-report' },
        { label: 'Analytics', key: '/admin/analytics', path: '/admin/analytics' }
      ]

  const userMenu = {
    onClick: ({ key }: { key: string }) => {
      if (key === 'logout') handleLogout()
      if (key === 'profile') navigate(
        role === 'doctor' ? '/doctor/profile' :
        role === 'patient' ? '/patient/profile' :
        '/admin/settings'
      )
    },
    items: [
      { key: 'profile', label: 'Profile Settings' },
      { key: 'logout', label: 'Logout' },
    ]
  }

  return (
    <Header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary-500 to-secondary-500 p-2 rounded-lg">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <span className="text-lg font-semibold">Med Triage</span>
          </Link>
        </div>

        <div className="hidden md:flex items-center">
          <Menu mode="horizontal" selectedKeys={[location.pathname]} items={navLinks.map((l) => ({ key: l.key, label: <Link to={l.path}>{l.label}</Link> }))} />
        </div>

        <div className="flex items-center gap-4">
          <Space align="center">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-slate-100 rounded-md">
              <User className="h-4 w-4 text-slate-600" />
              <span className="capitalize text-sm">{role}</span>
            </div>
            <Dropdown menu={userMenu} placement="bottomRight">
              <Avatar style={{ backgroundColor: '#00A86B' }}>
                {role ? role.charAt(0).toUpperCase() : 'U'}
              </Avatar>
            </Dropdown>
          </Space>
        </div>
      </div>
    </Header>
  )
}
