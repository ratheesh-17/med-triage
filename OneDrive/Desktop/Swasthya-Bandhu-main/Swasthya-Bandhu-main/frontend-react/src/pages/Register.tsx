import { useState } from 'react'
import { Card, Form, Input, Button, Select, Checkbox, Typography, Divider } from 'antd'
import { UserOutlined, PhoneOutlined, HeartOutlined } from '@ant-design/icons'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '../services/auth'
import toast from 'react-hot-toast'

const { Title, Paragraph, Text } = Typography
const { Option } = Select

export default function Register() {
  const [form] = Form.useForm()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  const onFinish = async (values: any) => {
    setLoading(true)
    try {
      const resp = await authService.registerPatient({
        phone: values.phone,
        name: values.name,
        age: Number(values.age),
        gender: values.gender
      })

      if (resp?.token) {
        authService.setAuth(resp.token, 'patient')
        toast.success('Account created successfully!')
        navigate('/patient/dashboard')
      }
    } catch (err: any) {
      toast.error(err?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-4">
      <Card style={{ width: '100%', maxWidth: 600, borderRadius: 16, boxShadow: '0 4px 24px rgba(0,0,0,0.1)' }}>
        <div className="text-center mb-6">
          <HeartOutlined style={{ fontSize: 48, color: '#1890FF', marginBottom: 16 }} />
          <Title level={2} className="!mb-2">Create Your Account</Title>
          <Paragraph className="text-gray-500">Join Med Triage for AI-powered health assistance</Paragraph>
        </div>

        <Form form={form} layout="vertical" onFinish={onFinish} size="large">
          <Form.Item
            name="name"
            label="Full Name"
            rules={[{ required: true, message: 'Please enter your full name' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="Enter your full name" />
          </Form.Item>

          <Form.Item
            name="phone"
            label="Phone Number"
            rules={[
              { required: true, message: 'Please enter your phone number' },
              { pattern: /^[0-9]{10}$/, message: 'Please enter a valid 10-digit phone number' }
            ]}
          >
            <Input
              prefix={<PhoneOutlined />}
              addonBefore="+91"
              placeholder="10-digit mobile number"
              maxLength={10}
            />
          </Form.Item>

          <Form.Item
            name="age"
            label="Age"
            rules={[{ required: true, message: 'Please enter your age' }]}
          >
            <Input type="number" placeholder="Enter your age" min={1} max={120} />
          </Form.Item>

          <Form.Item
            name="gender"
            label="Gender"
            rules={[{ required: true, message: 'Please select your gender' }]}
          >
            <Select placeholder="Select gender">
              <Option value="male">Male</Option>
              <Option value="female">Female</Option>
              <Option value="other">Prefer not to say</Option>
            </Select>
          </Form.Item>

          <Divider>Emergency Contact (Optional)</Divider>

          <Form.Item name="emergency_contact_name" label="Emergency Contact Name">
            <Input prefix={<UserOutlined />} placeholder="Contact person name" />
          </Form.Item>

          <Form.Item name="emergency_contact_phone" label="Emergency Contact Phone">
            <Input
              prefix={<PhoneOutlined />}
              addonBefore="+91"
              placeholder="10-digit mobile number"
              maxLength={10}
            />
          </Form.Item>

          <Form.Item
            name="agreement"
            valuePropName="checked"
            rules={[
              {
                validator: (_, value) =>
                  value ? Promise.resolve() : Promise.reject(new Error('Please accept the terms')),
              },
            ]}
          >
            <Checkbox>
              I agree that this platform provides <strong>triage assistance</strong> and not medical diagnosis
            </Checkbox>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading} className="!h-12">
              Create My Account
            </Button>
          </Form.Item>
        </Form>

        <div className="text-center mt-4">
          <Text className="text-gray-500">
            Already registered?{' '}
            <Link to="/login" className="text-blue-600 font-medium">
              Login here
            </Link>
          </Text>
        </div>
      </Card>
    </div>
  )
}
