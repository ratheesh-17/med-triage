import { Card, Typography, Tag, Descriptions, Button } from 'antd'
import { ClockCircleOutlined, CheckCircleOutlined, PhoneOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Title, Paragraph, Text } = Typography

const PENDING_DOCTOR_DATA = {
  fullName: 'Dr. Meera Sharma',
  phone: '+91 9876543210',
  email: 'meera.sharma@example.com',
  specialization: 'Cardiologist',
  medicalCouncilNumber: 'MCI/12345/2020',
  experience: 15,
  hospitalAffiliation: 'Apollo Hospital',
  submittedDate: '2024-01-15'
}

export default function DoctorPending() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-6">
      <Card className="max-w-3xl w-full shadow-xl">
        <div className="text-center mb-6">
          <ClockCircleOutlined style={{ fontSize: 80, color: '#faad14' }} />
          <Title level={2} className="!mt-6 !mb-4">Account Under Review</Title>
          <Tag color="orange" className="text-lg px-4 py-2">
            <ClockCircleOutlined className="mr-2" />
            Pending Verification
          </Tag>
        </div>

        <Card className="bg-yellow-50 border-yellow-200 mb-6">
          <Paragraph className="!mb-0 text-center text-lg">
            Your Medical Council Number is under review. You will be notified once approved.
            This typically takes <Text strong>24 hours</Text>.
          </Paragraph>
        </Card>

        <Descriptions title="Submitted Details" bordered column={1} className="mb-6">
          <Descriptions.Item label="Full Name">{PENDING_DOCTOR_DATA.fullName}</Descriptions.Item>
          <Descriptions.Item label="Phone Number">{PENDING_DOCTOR_DATA.phone}</Descriptions.Item>
          <Descriptions.Item label="Email">{PENDING_DOCTOR_DATA.email}</Descriptions.Item>
          <Descriptions.Item label="Specialization">{PENDING_DOCTOR_DATA.specialization}</Descriptions.Item>
          <Descriptions.Item label="Medical Council Number">
            <Text strong className="text-blue-600">{PENDING_DOCTOR_DATA.medicalCouncilNumber}</Text>
          </Descriptions.Item>
          <Descriptions.Item label="Years of Experience">{PENDING_DOCTOR_DATA.experience} years</Descriptions.Item>
          <Descriptions.Item label="Hospital Affiliation">{PENDING_DOCTOR_DATA.hospitalAffiliation}</Descriptions.Item>
          <Descriptions.Item label="Submitted On">{PENDING_DOCTOR_DATA.submittedDate}</Descriptions.Item>
        </Descriptions>

        <Card className="bg-blue-50 border-blue-200 mb-6">
          <div className="flex items-start gap-3">
            <CheckCircleOutlined className="text-blue-600 text-2xl mt-1" />
            <div>
              <Title level={5} className="!mb-2">What happens next?</Title>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                <li>Our admin team will verify your Medical Council Registration Number</li>
                <li>You will receive an OTP on your registered phone number once approved</li>
                <li>Use the OTP to login and access your doctor dashboard</li>
                <li>Start managing appointments and helping patients immediately</li>
              </ul>
            </div>
          </div>
        </Card>

        <div className="flex justify-center gap-4">
          <Button size="large" onClick={() => navigate('/login')}>
            Back to Login
          </Button>
          <Button type="primary" size="large" icon={<PhoneOutlined />}>
            Contact Support
          </Button>
        </div>
      </Card>
    </div>
  )
}
