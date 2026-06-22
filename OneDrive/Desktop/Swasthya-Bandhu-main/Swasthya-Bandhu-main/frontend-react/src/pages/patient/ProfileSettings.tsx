import { useState } from 'react'
import { Card, Form, Input, Button, Typography, Divider, Popconfirm, Space } from 'antd'
import { UserOutlined, PhoneOutlined, LogoutOutlined, DeleteOutlined, SaveOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { authService } from '../../services/auth'
import toast from 'react-hot-toast'

const { Title, Text } = Typography

export default function ProfileSettings() {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)

  const handleUpdateProfile = async () => {
    setLoading(true)
    try {
      // API call would go here
      toast.success('Profile updated successfully')
    } catch (error) {
      toast.error('Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    authService.logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const handleDeleteAccount = async () => {
    try {
      // API call would go here
      authService.logout()
      toast.success('Account deleted successfully')
      navigate('/')
    } catch (error) {
      toast.error('Failed to delete account')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto">
        <Title level={2} className="!mb-6">Profile Settings</Title>

        {/* Profile Information */}
        <Card title="Profile Information" style={{ borderRadius: 12, marginBottom: 16 }}>
          <Form
            form={form}
            layout="vertical"
            onFinish={handleUpdateProfile}
            initialValues={{
              name: 'John Doe',
              phone: '9876543210',
              age: 30,
              gender: 'male'
            }}
          >
            <Form.Item name="name" label="Full Name" rules={[{ required: true }]}>
              <Input prefix={<UserOutlined />} size="large" />
            </Form.Item>

            <Form.Item name="phone" label="Phone Number">
              <Input prefix={<PhoneOutlined />} size="large" disabled />
            </Form.Item>

            <Form.Item name="age" label="Age" rules={[{ required: true }]}>
              <Input type="number" size="large" />
            </Form.Item>

            <Form.Item name="gender" label="Gender" rules={[{ required: true }]}>
              <Input size="large" disabled />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                Save Changes
              </Button>
            </Form.Item>
          </Form>
        </Card>

        {/* Emergency Contacts */}
        <Card title="Emergency Contacts" style={{ borderRadius: 12, marginBottom: 16 }}>
          <Form layout="vertical">
            <Form.Item label="Primary Emergency Contact">
              <Input placeholder="Contact Name" size="large" className="mb-2" />
              <Input placeholder="Phone Number" size="large" />
            </Form.Item>

            <Form.Item label="Secondary Emergency Contact (Optional)">
              <Input placeholder="Contact Name" size="large" className="mb-2" />
              <Input placeholder="Phone Number" size="large" />
            </Form.Item>

            <Form.Item>
              <Button type="primary" icon={<SaveOutlined />}>
                Update Emergency Contacts
              </Button>
            </Form.Item>
          </Form>
        </Card>

        {/* Account Actions */}
        <Card title="Account Actions" style={{ borderRadius: 12 }}>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div>
              <Text strong className="block mb-2">Logout</Text>
              <Text className="text-gray-500 block mb-3">
                Sign out of your account on this device
              </Text>
              <Button icon={<LogoutOutlined />} onClick={handleLogout}>
                Logout
              </Button>
            </div>

            <Divider />

            <div>
              <Text strong className="block mb-2 text-red-600">Delete Account</Text>
              <Text className="text-gray-500 block mb-3">
                Permanently delete your account and all associated data. This action cannot be undone.
              </Text>
              <Popconfirm
                title="Delete Account?"
                description="Are you sure? This will permanently delete all your data."
                onConfirm={handleDeleteAccount}
                okText="Yes, Delete"
                cancelText="Cancel"
                okButtonProps={{ danger: true }}
              >
                <Button danger icon={<DeleteOutlined />}>
                  Delete Account
                </Button>
              </Popconfirm>
            </div>
          </Space>
        </Card>
      </div>
    </div>
  )
}
