import { useState, useEffect } from 'react'
import { Card, Row, Col, Button, Tag, Typography, Calendar, Modal, Rate, Progress, Spin } from 'antd'
import { ClockCircleOutlined, CheckCircleOutlined, StarOutlined, UserOutlined, VideoCameraOutlined, EnvironmentOutlined, WarningOutlined } from '@ant-design/icons'
import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text, Paragraph } = Typography

const WEEKLY_DATA = [
  { day: 'Mon', appointments: 12 },
  { day: 'Tue', appointments: 15 },
  { day: 'Wed', appointments: 10 },
  { day: 'Thu', appointments: 18 },
  { day: 'Fri', appointments: 14 },
  { day: 'Sat', appointments: 8 },
  { day: 'Sun', appointments: 5 }
]

const SEVERITY_DATA = [
  { name: 'Low (1-4)', value: 45, color: '#52c41a' },
  { name: 'Moderate (5-6)', value: 30, color: '#faad14' },
  { name: 'High (7-8)', value: 20, color: '#ff7a45' },
  { name: 'Emergency (9-10)', value: 5, color: '#f5222d' }
]

const FEEDBACK = [
  { patient: 'Meera Singh', rating: 5, comment: 'Very thorough examination and clear explanation' },
  { patient: 'Karthik Reddy', rating: 5, comment: 'Excellent doctor, highly recommend' },
  { patient: 'Anjali Nair', rating: 4, comment: 'Good consultation, helpful advice' }
]

export default function DoctorDashboard() {
  const [selectedAppointment, setSelectedAppointment] = useState<any>(null)
  const [triageModal, setTriageModal] = useState(false)
  const [doctor, setDoctor] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [appointments, setAppointments] = useState<any[]>([])
  const [completing, setCompleting] = useState<number | null>(null)
  const [dashboardStats, setDashboardStats] = useState<any>(null)

  useEffect(() => {
    loadDoctorProfile()
    loadAppointments()
    loadDashboardStats()
  }, [])

  const loadDashboardStats = async () => {
    try {
      const response = await api.get('/doctor/dashboard')
      setDashboardStats(response.data)
    } catch (error) {
      console.error('Failed to load dashboard stats')
    }
  }

  const loadDoctorProfile = async () => {
    try {
      const response = await api.get('/doctor/profile')
      setDoctor(response.data)
    } catch (error) {
      toast.error('Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const loadAppointments = async () => {
    try {
      const response = await api.get('/appointments')
      console.log('=== APPOINTMENTS API RESPONSE ===')
      console.log('Full response:', response.data)
      console.log('Appointments array:', response.data.appointments)
      console.log('Total appointments:', response.data.appointments?.length || 0)
      if (response.data.appointments?.length > 0) {
        console.log('First appointment:', response.data.appointments[0])
        console.log('Has pre_consult_summary?', !!response.data.appointments[0].pre_consult_summary)
      }
      setAppointments(response.data.appointments || [])
    } catch (error) {
      console.error('Failed to load appointments', error)
    }
  }

  const handleMarkComplete = async (appointmentId: number) => {
    setCompleting(appointmentId)
    try {
      await api.patch(`/appointments/${appointmentId}/complete`)
      toast.success('Appointment marked as completed')
      loadAppointments()
    } catch (error) {
      toast.error('Failed to mark appointment as complete')
    } finally {
      setCompleting(null)
    }
  }

  const handleStartConsultation = async () => {
    if (!selectedAppointment) return
    try {
      await api.patch(`/appointments/${selectedAppointment.id}/start`)
      toast.success('Consultation started! Status updated to In-Progress')
      setTriageModal(false)
      loadAppointments()
    } catch (error) {
      toast.error('Failed to start consultation')
    }
  }

  const getSeverityColor = (severity: number) => {
    if (severity <= 4) return 'green'
    if (severity <= 6) return 'orange'
    if (severity <= 8) return 'red'
    return 'red'
  }

  const getUrgencyColor = (urgency: string) => {
    if (urgency === 'Emergency') return 'red'
    if (urgency === 'High') return 'orange'
    return 'green'
  }

  const handleViewTriage = (appointment: any) => {
    setSelectedAppointment(appointment)
    setTriageModal(true)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <Title level={2}>Doctor Dashboard</Title>
          <Text className="text-gray-500">Welcome back, Dr. {doctor?.name || 'Doctor'}</Text>
        </div>

        {/* Today's Overview */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <ClockCircleOutlined style={{ fontSize: 32, color: '#1890ff' }} />
              <Title level={3} className="!mt-4 !mb-0">{dashboardStats?.today_cases || 0}</Title>
              <Text className="text-gray-500">Total Today</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <CheckCircleOutlined style={{ fontSize: 32, color: '#52c41a' }} />
              <Title level={3} className="!mt-4 !mb-0">{appointments.filter(a => a.status === 'completed').length}</Title>
              <Text className="text-gray-500">Completed</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <UserOutlined style={{ fontSize: 32, color: '#faad14' }} />
              <Title level={3} className="!mt-4 !mb-0">{appointments.filter(a => a.status === 'scheduled').length}</Title>
              <Text className="text-gray-500">Pending</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <StarOutlined style={{ fontSize: 32, color: '#ff7a45' }} />
              <Title level={3} className="!mt-4 !mb-0">{doctor?.rating || 0}</Title>
              <Text className="text-gray-500">Platform Rating</Text>
            </Card>
          </Col>
        </Row>

        {/* Today's Appointment Queue */}
        <Card title="Today's Appointment Queue" className="mb-6 shadow-sm">
          {(() => {
            const activeAppointments = appointments.filter(a => a.status === 'scheduled' || a.status === 'in-progress')
            return activeAppointments.length === 0 ? (
              <Text className="text-gray-500">No pending appointments</Text>
            ) : (
              <div className="space-y-4">
                {activeAppointments.map(apt => (
                <Card key={apt.id} className="border-l-4" style={{ borderLeftColor: apt.pre_consult_summary?.severity_score ? getSeverityColor(apt.pre_consult_summary.severity_score) : '#d9d9d9' }}>
                  <Row gutter={16} align="middle">
                    <Col flex="100px">
                      <Text strong className="text-lg">{apt.time}</Text>
                    </Col>
                    <Col flex="auto">
                      <div className="flex items-center gap-2 mb-2">
                        <Text strong className="text-base">{apt.patient?.name}, {apt.patient?.age}y</Text>
                        <Tag color={apt.slot_type === 'online' ? 'blue' : 'green'} icon={apt.slot_type === 'online' ? <VideoCameraOutlined /> : <EnvironmentOutlined />}>
                          {apt.slot_type === 'online' ? 'Online' : 'In-Person'}
                        </Tag>
                        {apt.pre_consult_summary && (
                          <>
                            <Tag color={getSeverityColor(apt.pre_consult_summary.severity_score)}>Severity: {apt.pre_consult_summary.severity_score}/10</Tag>
                            <Tag color={getUrgencyColor(apt.pre_consult_summary.urgency)}>{apt.pre_consult_summary.urgency}</Tag>
                          </>
                        )}
                      </div>
                      <Text className="text-gray-600">Symptoms: {apt.symptom_notes || 'Not specified'}</Text>
                      {apt.payment_amount && (
                        <div className="mt-2">
                          <Tag color="green">₹{apt.payment_amount} Paid</Tag>
                        </div>
                      )}
                    </Col>
                    <Col>
                      {apt.pre_consult_summary && apt.status === 'scheduled' && (
                        <Button type="primary" onClick={() => handleViewTriage(apt)} className="mr-2">
                          View Full Triage
                        </Button>
                      )}
                      {apt.status === 'in-progress' ? (
                        <Button
                          type="primary"
                          style={{ background: '#52c41a', borderColor: '#52c41a' }}
                          icon={<CheckCircleOutlined />}
                          onClick={() => handleMarkComplete(apt.id)}
                          loading={completing === apt.id}
                        >
                          End Consultation
                        </Button>
                      ) : (
                        <Button
                          onClick={() => handleMarkComplete(apt.id)}
                          loading={completing === apt.id}
                        >
                          Mark Complete
                        </Button>
                      )}
                    </Col>
                  </Row>
                </Card>
              ))}
            </div>
          )})()}
        </Card>

        <Row gutter={[16, 16]}>
          {/* Upcoming Appointments */}
          <Col xs={24} lg={12}>
            <Card title="Upcoming Appointments" className="shadow-sm">
              <Calendar fullscreen={false} />
            </Card>
          </Col>

          {/* Weekly Performance */}
          <Col xs={24} lg={12}>
            <Card title="Weekly Performance" className="shadow-sm mb-4">
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={WEEKLY_DATA}>
                  <XAxis dataKey="day" />
                  <YAxis />
                  <RechartsTooltip />
                  <Bar dataKey="appointments" fill="#1890ff" />
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card title="Severity Distribution" className="shadow-sm mb-4">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={SEVERITY_DATA} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80}>
                    {SEVERITY_DATA.map((entry, index) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            <Card className="shadow-sm">
              <Row gutter={16}>
                <Col span={12}>
                  <Text className="text-gray-500">Avg Response Time</Text>
                  <Title level={4} className="!mt-1 !mb-0">12 mins</Title>
                </Col>
                <Col span={12}>
                  <Text className="text-gray-500">Patient Return Rate</Text>
                  <Title level={4} className="!mt-1 !mb-0">78%</Title>
                </Col>
              </Row>
            </Card>
          </Col>
        </Row>

        {/* Recent Feedback */}
        <Card title="Recent Patient Feedback" className="mt-6 shadow-sm">
          <div className="space-y-4">
            {FEEDBACK.map((fb, idx) => (
              <div key={idx} className="border-b pb-4 last:border-b-0">
                <div className="flex items-center justify-between mb-2">
                  <Text strong>{fb.patient}</Text>
                  <Rate disabled defaultValue={fb.rating} />
                </div>
                <Text className="text-gray-600">{fb.comment}</Text>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* AI Triage Modal */}
      <Modal
        title="AI Pre-Consult Summary"
        open={triageModal}
        onCancel={() => setTriageModal(false)}
        width={900}
        footer={[
          <Button key="close" onClick={() => setTriageModal(false)}>Close</Button>,
          <Button key="start" type="primary" onClick={handleStartConsultation}>Start Consultation</Button>
        ]}
      >
        {selectedAppointment && (
          <Row gutter={16}>
            <Col span={10}>
              <Card title="Patient Information" size="small" className="mb-4">
                <p><Text strong>Name:</Text> {selectedAppointment.patient?.name}</p>
                <p><Text strong>Age:</Text> {selectedAppointment.patient?.age} years</p>
                <p><Text strong>Gender:</Text> {selectedAppointment.patient?.gender}</p>
              </Card>
              {selectedAppointment.pre_consult_summary?.risk_factors && (
                <Card title="Risk Factors" size="small">
                  <ul className="list-disc pl-4">
                    {selectedAppointment.pre_consult_summary.risk_factors.map((risk: string, idx: number) => (
                      <li key={idx}>{risk}</li>
                    ))}
                  </ul>
                </Card>
              )}
            </Col>
            <Col span={14}>
              {selectedAppointment.pre_consult_summary ? (
                <Card title="AI Triage Analysis" size="small">
                  <div className="mb-4">
                    <Text strong>Symptoms:</Text>
                    <Paragraph className="!mb-2">{selectedAppointment.symptom_notes}</Paragraph>
                  </div>
                  <div className="mb-4">
                    <Text strong>Severity Score:</Text>
                    <div className="flex items-center gap-4 mt-2">
                      <Progress type="circle" percent={selectedAppointment.pre_consult_summary.severity_score * 10} width={80} strokeColor={getSeverityColor(selectedAppointment.pre_consult_summary.severity_score)} />
                      <Tag color={getUrgencyColor(selectedAppointment.pre_consult_summary.urgency)} className="text-lg px-4 py-1">{selectedAppointment.pre_consult_summary.urgency}</Tag>
                    </div>
                  </div>
                  {selectedAppointment.pre_consult_summary.severity_score >= 9 && (
                    <Card size="small" className="mb-4 border-red-500 bg-red-50">
                      <div className="flex items-start gap-2">
                        <WarningOutlined className="text-red-500 text-xl" />
                        <div>
                          <Text strong className="text-red-600">Red Flag Indicators</Text>
                          <Paragraph className="!mb-0 text-red-600">Immediate evaluation required. Consider emergency protocols.</Paragraph>
                        </div>
                      </div>
                    </Card>
                  )}
                  {selectedAppointment.pre_consult_summary.suggested_tests && (
                    <div className="mb-4">
                      <Text strong>Suggested Tests:</Text>
                      <ul className="list-disc pl-4 mt-2">
                        {selectedAppointment.pre_consult_summary.suggested_tests.map((test: string, idx: number) => (
                          <li key={idx}>{test}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {selectedAppointment.pre_consult_summary.differential_diagnoses && (
                    <div className="mb-4">
                      <Text strong>Differential Diagnoses:</Text>
                      <ul className="list-disc pl-4 mt-2">
                        {selectedAppointment.pre_consult_summary.differential_diagnoses.map((diagnosis: string, idx: number) => (
                          <li key={idx}>{diagnosis}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </Card>
              ) : (
                <Card title="Appointment Details" size="small">
                  <Text>No AI pre-consultation summary available for this appointment.</Text>
                </Card>
              )}
            </Col>
          </Row>
        )}
      </Modal>
    </div>
  )
}
