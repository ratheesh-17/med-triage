import { useState } from 'react'
import { Card, Form, Input, Button, Upload, Row, Col, Typography, Tag, Checkbox, Tooltip, Alert } from 'antd'
import { UserOutlined, UploadOutlined, LockOutlined, CheckCircleOutlined, SaveOutlined } from '@ant-design/icons'
import toast from 'react-hot-toast'

const { Title, Text } = Typography
const { TextArea } = Input

const INITIAL_DATA = {
  fullName: 'Dr. Meera Sharma',
  phone: '+91 9876543210',
  email: 'meera.sharma@example.com',
  specialization: 'Cardiologist',
  medicalCouncilNumber: 'MCI/12345/2020',
  experience: 15,
  hospitalAffiliation: 'Apollo Hospital',
  consultationFee: 800,
  consultationDuration: 30,
  consultationTypes: ['online', 'in-person'],
  bio: 'Experienced cardiologist with 15 years of practice. Specialized in interventional cardiology and preventive cardiac care.',
  profilePhoto: ''
}

export default function DoctorProfile() {
  const [form] = Form.useForm()
  const [profilePhoto, setProfilePhoto] = useState<string>('')
  const [isEditing, setIsEditing] = useState(false)

  const handlePhotoUpload = (file: File) => {
    const reader = new FileReader()
    reader.onload = (e) => setProfilePhoto(e.target?.result as string)
    reader.readAsDataURL(file)
    return false
  }

  const handleSave = async (values: any) => {
    try {
      console.log('Updated profile:', values)
      toast.success('Profile updated successfully')
      setIsEditing(false)
    } catch (err) {
      toast.error('Failed to update profile')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Title level={2}>Profile Management</Title>
          {!isEditing ? (
            <Button type="primary" onClick={() => setIsEditing(true)}>
              Edit Profile
            </Button>
          ) : (
            <Button onClick={() => setIsEditing(false)}>
              Cancel
            </Button>
          )}
        </div>

        {/* Verification Status Banner */}
        <Alert
          message={
            <div className="flex items-center gap-2">
              <CheckCircleOutlined style={{ fontSize: 20 }} />
              <Text strong>Verified Doctor</Text>
            </div>
          }
          description="Your Medical Council credentials have been verified by our admin team"
          type="success"
          showIcon={false}
          className="mb-6"
        />

        <Card className="shadow-sm">
          <Form
            form={form}
            layout="vertical"
            initialValues={INITIAL_DATA}
            onFinish={handleSave}
            disabled={!isEditing}
          >
            {/* Profile Photo */}
            <div className="text-center mb-6">
              <Upload
                accept="image/*"
                showUploadList={false}
                beforeUpload={handlePhotoUpload}
                disabled={!isEditing}
              >
                <div className="cursor-pointer">
                  {profilePhoto || INITIAL_DATA.profilePhoto ? (
                    <img 
                      src={profilePhoto || INITIAL_DATA.profilePhoto} 
                      alt="Profile" 
                      className="w-32 h-32 rounded-full mx-auto object-cover border-4 border-blue-200" 
                    />
                  ) : (
                    <div className="w-32 h-32 rounded-full mx-auto bg-blue-100 flex items-center justify-center border-4 border-blue-300">
                      <UserOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                    </div>
                  )}
                  {isEditing && (
                    <Button icon={<UploadOutlined />} className="mt-4">
                      Change Photo
                    </Button>
                  )}
                </div>
              </Upload>
            </div>

            <Row gutter={16}>
              {/* Basic Information */}
              <Col span={24}>
                <Title level={4} className="!mb-4">Basic Information</Title>
              </Col>
              
              <Col span={12}>
                <Form.Item name="fullName" label="Full Name" rules={[{ required: true }]}>
                  <Input />
                </Form.Item>
              </Col>
              
              <Col span={12}>
                <Form.Item name="phone" label="Phone Number" rules={[{ required: true }]}>
                  <Input disabled />
                </Form.Item>
              </Col>
              
              <Col span={12}>
                <Form.Item name="email" label="Email Address" rules={[{ required: true, type: 'email' }]}>
                  <Input />
                </Form.Item>
              </Col>
              
              <Col span={12}>
                <Form.Item name="experience" label="Years of Experience">
                  <Input disabled />
                </Form.Item>
              </Col>

              {/* Professional Credentials (Locked) */}
              <Col span={24} className="mt-6">
                <Title level={4} className="!mb-4">
                  Professional Credentials
                  <Tag color="green" className="ml-3">Verified</Tag>
                </Title>
              </Col>
              
              <Col span={12}>
                <Form.Item 
                  name="specialization" 
                  label={
                    <span>
                      Medical Specialization{' '}
                      <Tooltip title="Contact support to update verified credentials">
                        <LockOutlined className="text-gray-400" />
                      </Tooltip>
                    </span>
                  }
                >
                  <Input disabled suffix={<LockOutlined className="text-gray-400" />} />
                </Form.Item>
              </Col>
              
              <Col span={12}>
                <Form.Item 
                  name="medicalCouncilNumber" 
                  label={
                    <span>
                      Medical Council Number{' '}
                      <Tooltip title="Contact support to update verified credentials">
                        <LockOutlined className="text-gray-400" />
                      </Tooltip>
                    </span>
                  }
                >
                  <Input disabled suffix={<LockOutlined className="text-gray-400" />} />
                </Form.Item>
              </Col>
              
              <Col span={24}>
                <Form.Item name="hospitalAffiliation" label="Hospital/Clinic Affiliation">
                  <Input />
                </Form.Item>
              </Col>

              {/* Consultation Details */}
              <Col span={24} className="mt-6">
                <Title level={4} className="!mb-4">Consultation Details</Title>
              </Col>
              
              <Col span={12}>
                <Form.Item name="consultationFee" label="Consultation Fee (₹)" rules={[{ required: true }]}>
                  <Input type="number" prefix="₹" />
                </Form.Item>
              </Col>
              
              <Col span={12}>
                <Form.Item name="consultationDuration" label="Avg Duration (minutes)" rules={[{ required: true }]}>
                  <Input type="number" suffix="mins" />
                </Form.Item>
              </Col>
              
              <Col span={24}>
                <Form.Item name="consultationTypes" label="Consultation Types">
                  <Checkbox.Group>
                    <Checkbox value="online">Online</Checkbox>
                    <Checkbox value="in-person">In-Person</Checkbox>
                  </Checkbox.Group>
                </Form.Item>
              </Col>

              {/* Professional Bio */}
              <Col span={24} className="mt-6">
                <Title level={4} className="!mb-4">Professional Bio</Title>
              </Col>
              
              <Col span={24}>
                <Form.Item name="bio" label="Bio" rules={[{ required: true }]}>
                  <TextArea rows={4} maxLength={300} showCount />
                </Form.Item>
              </Col>
            </Row>

            {isEditing && (
              <div className="flex justify-end gap-2 mt-6">
                <Button onClick={() => setIsEditing(false)}>
                  Cancel
                </Button>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                  Save Changes
                </Button>
              </div>
            )}
          </Form>
        </Card>

        {/* Additional Info */}
        <Card className="mt-6 shadow-sm bg-blue-50 border-blue-200">
          <Text className="text-blue-700">
            <LockOutlined className="mr-2" />
            To update your Medical Council Number or Specialization, please contact our support team at support@swasthyabandhu.com
          </Text>
        </Card>
      </div>
    </div>
  )
}
