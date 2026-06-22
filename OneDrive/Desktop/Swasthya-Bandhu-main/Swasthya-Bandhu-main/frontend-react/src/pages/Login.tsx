import { useState } from 'react'
import { Form, Input, Button, Typography } from 'antd'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/auth'
import toast from 'react-hot-toast'
import { PhoneOutlined, LockOutlined, HeartOutlined, SafetyOutlined, LineChartOutlined } from '@ant-design/icons'

const { Title, Paragraph } = Typography

export default function Login() {
  const [form] = Form.useForm()
  const navigate = useNavigate()
  const [showOtpField, setShowOtpField] = useState(false)
  const [adminPhone, setAdminPhone] = useState('')

  const handleLogin = async (values: { phone: string; otp?: string }) => {
    try {
      // For admin, verify OTP
      if (showOtpField && values.otp) {
        const resp = await authService.verifyAdminOTP(adminPhone, values.otp)
        if (resp?.token && resp?.role) {
          authService.setAuth(resp.token, resp.role)
          toast.success('Admin logged in')
          navigate('/admin/dashboard')
        }
      } else {
        // Initial login request
        const resp = await authService.login(values.phone)
        
        if (resp?.otp_sent) {
          // Admin flow - OTP was sent
          setAdminPhone(values.phone)
          setShowOtpField(true)
          toast.success('OTP sent to your phone')
        } else if (resp?.token && resp?.role) {
          // Patient/Doctor direct login
          authService.setAuth(resp.token, resp.role)
          toast.success('Logged in')
          if (resp.role === 'patient') navigate('/patient/dashboard')
          else if (resp.role === 'doctor') navigate('/doctor/dashboard')
          else navigate('/admin/dashboard')
        } else {
          toast.error('Login failed')
        }
      }
    } catch (err: any) {
      toast.error(err?.message || 'Login error')
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left: 75% - Branding Section */}
      <div className="hidden lg:flex lg:w-3/4 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDE0YzMuMzEgMCA2IDIuNjkgNiA2cy0yLjY5IDYtNiA2LTYtMi42OS02LTYgMi42OS02IDYtNnpNNiAzNGMzLjMxIDAgNiAyLjY5IDYgNnMtMi42OSA2LTYgNi02LTIuNjktNi02IDIuNjktNiA2LTZ6TTM2IDM0YzMuMzEgMCA2IDIuNjkgNiA2cy0yLjY5IDYtNiA2LTYtMi42OS02LTYgMi42OS02IDYtNnoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30"></div>
        
        <div className="relative z-10 flex flex-col justify-center px-16 py-12 text-white">
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-white/10 backdrop-blur-sm p-3 rounded-xl">
                <HeartOutlined style={{ fontSize: 32, color: 'white' }} />
              </div>
              <Title level={2} className="!text-white !mb-0">Med Triage</Title>
            </div>
            <Title level={1} className="!text-white !text-5xl !mb-4 !leading-tight">
              Your AI-Powered<br />Healthcare Companion
            </Title>
            <Paragraph className="!text-white/90 text-xl max-w-2xl">
              Instant symptom analysis, trusted doctor matching, and comprehensive health tracking.
              Secure, private, and clinically-informed care for you and your family.
            </Paragraph>
          </div>

          <div className="grid grid-cols-3 gap-6 mt-12">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <SafetyOutlined style={{ fontSize: 36, color: 'white', marginBottom: 16 }} />
              <Title level={4} className="!text-white !mb-2">AI Diagnosis</Title>
              <Paragraph className="!text-white/80 !mb-0">Clinical-grade symptom triage powered by advanced AI</Paragraph>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <PhoneOutlined style={{ fontSize: 36, color: 'white', marginBottom: 16 }} />
              <Title level={4} className="!text-white !mb-2">Smart Appointments</Title>
              <Paragraph className="!text-white/80 !mb-0">Connect with verified doctors near you instantly</Paragraph>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <LineChartOutlined style={{ fontSize: 36, color: 'white', marginBottom: 16 }} />
              <Title level={4} className="!text-white !mb-2">Health Insights</Title>
              <Paragraph className="!text-white/80 !mb-0">Track longitudinal health trends and risk factors</Paragraph>
            </div>
          </div>

          <div className="mt-16 flex items-center gap-8 text-white/70">
            <div>
              <div className="text-3xl font-bold text-white">10K+</div>
              <div className="text-sm">Active Users</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">500+</div>
              <div className="text-sm">Verified Doctors</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">98%</div>
              <div className="text-sm">Satisfaction Rate</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right: 25% - Login Form */}
      <div className="w-full lg:w-1/4 flex items-center justify-center bg-white px-8 py-12">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <Title level={3} className="!mb-2">
              {showOtpField ? 'Enter OTP' : 'Welcome Back'}
            </Title>
            <Paragraph className="text-gray-500">
              {showOtpField ? 'Enter the OTP sent to your phone' : 'Sign in to access your dashboard'}
            </Paragraph>
          </div>

          <Form form={form} layout="vertical" onFinish={handleLogin} size="large">
            {!showOtpField ? (
              <Form.Item 
                name="phone" 
                label="Phone Number" 
                rules={[{ required: true, message: 'Please enter your phone number' }]}
              >
                <Input 
                  prefix={<PhoneOutlined className="text-gray-400" />}
                  placeholder="Enter phone number" 
                />
              </Form.Item>
            ) : (
              <Form.Item 
                name="otp" 
                label="OTP" 
                rules={[{ required: true, message: 'Please enter OTP' }]}
              >
                <Input 
                  prefix={<LockOutlined className="text-gray-400" />}
                  placeholder="6-digit OTP" 
                  maxLength={6}
                />
              </Form.Item>
            )}

            <Form.Item className="!mb-4">
              <Button 
                type="primary" 
                htmlType="submit" 
                block 
                size="large"
                className="!h-12 !text-base"
              >
                {showOtpField ? 'Verify OTP' : 'Continue'}
              </Button>
            </Form.Item>
          </Form>

          {!showOtpField && (
            <>
              <div className="text-center mt-6">
                <Paragraph className="text-gray-500 !mb-2">Don't have an account?</Paragraph>
                <a href="/register" className="text-blue-600 font-medium hover:text-blue-700">
                  Create an account
                </a>
              </div>
              
              <div className="text-center mt-4">
                <Paragraph className="text-gray-500 !mb-2">Are you a doctor?</Paragraph>
                <a href="/doctor/register" className="text-blue-600 font-medium hover:text-blue-700">
                  Register as Doctor
                </a>
              </div>
              
              <div className="mt-8 pt-6 border-t border-gray-200">
                <Paragraph className="text-xs text-gray-400 text-center !mb-0">
                  By continuing, you agree to our Terms of Service and Privacy Policy
                </Paragraph>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
