import { Card, Row, Col, Typography, Timeline, Tag } from 'antd'
import { UserOutlined, HeartOutlined, MedicineBoxOutlined, TeamOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

const PATIENT_DATA = {
  name: 'Rajesh Kumar',
  age: 45,
  gender: 'Male',
  phone: '+91 9876543210',
  emergencyContact: '+91 9876543211',
  aiSessions: [
    {
      date: '2024-01-10',
      symptoms: 'Chest pain, shortness of breath',
      severity: 9,
      recommended: 'Cardiologist'
    },
    {
      date: '2024-01-05',
      symptoms: 'Mild fever, body ache',
      severity: 3,
      recommended: 'General Physician'
    },
    {
      date: '2023-12-20',
      symptoms: 'Persistent cough',
      severity: 5,
      recommended: 'Pulmonologist'
    }
  ],
  pastAppointments: [
    {
      date: '2024-01-08',
      doctor: 'Dr. Meera Singh',
      specialization: 'Cardiologist',
      type: 'In-Person'
    },
    {
      date: '2023-12-22',
      doctor: 'Dr. Amit Verma',
      specialization: 'Pulmonologist',
      type: 'Online'
    }
  ],
  family: [
    { name: 'Sunita Kumar', relation: 'Spouse', recentActivity: 'Routine checkup - 2024-01-12' },
    { name: 'Arjun Kumar', relation: 'Son', recentActivity: 'Vaccination - 2024-01-05' }
  ]
}

export default function PatientHistory() {
  const getSeverityColor = (severity: number) => {
    if (severity <= 4) return 'green'
    if (severity <= 6) return 'orange'
    if (severity <= 8) return 'red'
    return 'red'
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <Title level={2} className="mb-6">Patient History</Title>

        {/* Patient Basic Details */}
        <Card className="mb-6 shadow-sm">
          <Row gutter={16}>
            <Col span={1}>
              <div className="w-20 h-20 rounded-full bg-blue-100 flex items-center justify-center">
                <UserOutlined style={{ fontSize: 40, color: '#1890ff' }} />
              </div>
            </Col>
            <Col span={23}>
              <Title level={3} className="!mb-2">{PATIENT_DATA.name}</Title>
              <div className="grid grid-cols-4 gap-4">
                <div>
                  <Text className="text-gray-500">Age</Text>
                  <div><Text strong>{PATIENT_DATA.age} years</Text></div>
                </div>
                <div>
                  <Text className="text-gray-500">Gender</Text>
                  <div><Text strong>{PATIENT_DATA.gender}</Text></div>
                </div>
                <div>
                  <Text className="text-gray-500">Phone</Text>
                  <div><Text strong>{PATIENT_DATA.phone}</Text></div>
                </div>
                <div>
                  <Text className="text-gray-500">Emergency Contact</Text>
                  <div><Text strong>{PATIENT_DATA.emergencyContact}</Text></div>
                </div>
              </div>
            </Col>
          </Row>
        </Card>

        <Row gutter={[16, 16]}>
          {/* AI Sessions Timeline */}
          <Col xs={24} lg={12}>
            <Card 
              title={
                <span>
                  <HeartOutlined className="mr-2" />
                  AI Symptom Analysis History
                </span>
              }
              className="shadow-sm"
            >
              <Timeline>
                {PATIENT_DATA.aiSessions.map((session, idx) => (
                  <Timeline.Item key={idx} color={getSeverityColor(session.severity)}>
                    <div className="mb-4">
                      <Text strong className="block mb-1">{session.date}</Text>
                      <Paragraph className="!mb-2 text-gray-600">{session.symptoms}</Paragraph>
                      <div className="flex items-center gap-2">
                        <Tag color={getSeverityColor(session.severity)}>
                          Severity: {session.severity}/10
                        </Tag>
                        <Tag color="blue">→ {session.recommended}</Tag>
                      </div>
                    </div>
                  </Timeline.Item>
                ))}
              </Timeline>
            </Card>
          </Col>

          {/* Past Appointments */}
          <Col xs={24} lg={12}>
            <Card 
              title={
                <span>
                  <MedicineBoxOutlined className="mr-2" />
                  Past Appointments
                </span>
              }
              className="shadow-sm mb-4"
            >
              <div className="space-y-4">
                {PATIENT_DATA.pastAppointments.map((apt, idx) => (
                  <div key={idx} className="border-b pb-4 last:border-b-0">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <Text strong className="block">{apt.doctor}</Text>
                        <Text className="text-gray-500 text-sm">{apt.specialization}</Text>
                      </div>
                      <Tag color={apt.type === 'Online' ? 'blue' : 'green'}>{apt.type}</Tag>
                    </div>
                    <Text className="text-gray-400 text-xs">{apt.date}</Text>
                  </div>
                ))}
              </div>
            </Card>

            {/* Family Health Overview */}
            <Card 
              title={
                <span>
                  <TeamOutlined className="mr-2" />
                  Family Health Overview
                </span>
              }
              className="shadow-sm"
            >
              <div className="space-y-4">
                {PATIENT_DATA.family.map((member, idx) => (
                  <div key={idx} className="border-b pb-4 last:border-b-0">
                    <div className="flex justify-between items-start mb-1">
                      <Text strong>{member.name}</Text>
                      <Tag>{member.relation}</Tag>
                    </div>
                    <Text className="text-gray-500 text-sm">{member.recentActivity}</Text>
                  </div>
                ))}
              </div>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  )
}
