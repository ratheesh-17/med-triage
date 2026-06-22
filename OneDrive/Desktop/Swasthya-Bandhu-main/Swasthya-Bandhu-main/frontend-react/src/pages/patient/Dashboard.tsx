import { useState, useEffect } from 'react'
import { Row, Col, Card, Typography, Button, Input, Modal, Progress, Empty, Tag } from 'antd'
import {
  MessageOutlined,
  CalendarOutlined,
  LineChartOutlined,
  TeamOutlined,
  FileTextOutlined,
  PlusOutlined,
  AudioOutlined
} from '@ant-design/icons'
import api from '../../services/api'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

const { Title, Text } = Typography
const { TextArea } = Input

export default function PatientDashboard() {
  const navigate = useNavigate()
  const [userName, setUserName] = useState('Patient')
  const [symptoms, setSymptoms] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [healthRisk, setHealthRisk] = useState<any>(null)
  const [appointments, setAppointments] = useState<any[]>([])
  const [recentSessions, setRecentSessions] = useState<any[]>([])
  
  // Follow-up questions state
  const [showQuestions, setShowQuestions] = useState(false)
  const [questions, setQuestions] = useState<any[]>([])
  const [answers, setAnswers] = useState<any>({})

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      // Load user profile
      const profileResp = await api.get('/patient/profile')
      setUserName(profileResp.data.name)

      // Load health risk data
      const riskResp = await api.get('/health-risk')
      if (riskResp.data.has_data) {
        setHealthRisk(riskResp.data)
      }

      // Load appointments
      const aptResp = await api.get('/appointments')
      setAppointments(aptResp.data.appointments || [])

      // Load recent sessions
      const sessionsResp = await api.get('/patient/sessions')
      setRecentSessions(sessionsResp.data.sessions || [])
    } catch (error) {
      console.error('Failed to load dashboard data', error)
    }
  }

  const handleTriage = async () => {
    if (!symptoms.trim()) {
      toast.error('Please describe your symptoms')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/chat', { 
        symptom_text: symptoms,
        answers: showQuestions ? answers : null 
      })
      
      // Check if we need clarification
      if (response.data.needs_clarification) {
        setQuestions(response.data.questions)
        setShowQuestions(true)
        setAnswers({})
        toast('Please answer a few questions to help us assess your condition', { icon: 'ℹ️' })
      } else {
        setResult(response.data)
        setShowQuestions(false)
        
        if (response.data.is_emergency) {
          toast.error('EMERGENCY DETECTED! Please call 108 immediately', { duration: 10000 })
        } else {
          toast.success('Analysis complete!')
        }
        
        loadDashboardData() // Refresh data
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to analyze symptoms')
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (score: number) => {
    if (score >= 9) return '#f5222d'
    if (score >= 7) return '#fa8c16'
    if (score >= 5) return '#faad14'
    return '#52c41a'
  }

  const getSeverityLabel = (score: number) => {
    if (score >= 9) return 'Emergency'
    if (score >= 7) return 'High'
    if (score >= 5) return 'Moderate'
    return 'Low'
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2} className="!mb-6">Hello, {userName} 👋</Title>

        {/* Section 1: Symptom Input - PRIMARY ACTION */}
        <Card className="mb-6" style={{ borderRadius: 12, border: '2px solid #1890FF' }}>
          <div className="flex items-center gap-4 mb-4">
            <MessageOutlined style={{ fontSize: 32, color: '#1890FF' }} />
            <div>
              <Title level={4} className="!mb-0">Describe Your Symptoms</Title>
              <Text className="text-gray-500">Get instant AI-powered health assessment</Text>
            </div>
          </div>
          <TextArea
            rows={3}
            placeholder="E.g., I have a headache and fever for 2 days..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="mb-3"
          />
          <div className="flex gap-3">
            <Button
              type="primary"
              size="large"
              icon={<MessageOutlined />}
              onClick={handleTriage}
              loading={loading}
              block
            >
              Start AI Analysis
            </Button>
            <Button size="large" icon={<AudioOutlined />} />
          </div>
        </Card>

        <Row gutter={[16, 16]}>
          {/* Section 2: Health Risk Index */}
          <Col xs={24} lg={12}>
            <Card
              title={
                <div className="flex items-center gap-2">
                  <LineChartOutlined style={{ color: '#fa8c16' }} />
                  <span>Your Health Risk Index</span>
                </div>
              }
              style={{ borderRadius: 12, height: '100%' }}
            >
              {healthRisk?.has_data ? (
                <div>
                  <Row gutter={16}>
                    <Col span={12}>
                      <div className="mb-4">
                        <Text className="text-gray-500">Cardiac Risk</Text>
                        <Progress
                          percent={healthRisk.current_risk.cardiac * 10}
                          strokeColor="#f5222d"
                          showInfo={false}
                        />
                      </div>
                    </Col>
                    <Col span={12}>
                      <div className="mb-4">
                        <Text className="text-gray-500">Metabolic Risk</Text>
                        <Progress
                          percent={healthRisk.current_risk.metabolic * 10}
                          strokeColor="#fa8c16"
                          showInfo={false}
                        />
                      </div>
                    </Col>
                    <Col span={12}>
                      <div className="mb-4">
                        <Text className="text-gray-500">Neurological Risk</Text>
                        <Progress
                          percent={healthRisk.current_risk.neurological * 10}
                          strokeColor="#faad14"
                          showInfo={false}
                        />
                      </div>
                    </Col>
                    <Col span={12}>
                      <div className="mb-4">
                        <Text className="text-gray-500">Respiratory Risk</Text>
                        <Progress
                          percent={healthRisk.current_risk.respiratory * 10}
                          strokeColor="#1890ff"
                          showInfo={false}
                        />
                      </div>
                    </Col>
                  </Row>
                  <div className="mt-4 p-3 bg-blue-50 rounded">
                    <Text strong>Trend: </Text>
                    <Text>{healthRisk.current_risk.trend}</Text>
                  </div>
                </div>
              ) : (
                <Empty
                  description="Complete your first AI session to see your health trend"
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                />
              )}
            </Card>
          </Col>

          {/* Section 3: Upcoming Appointments */}
          <Col xs={24} lg={12}>
            <Card
              title={
                <div className="flex items-center gap-2">
                  <CalendarOutlined style={{ color: '#52c41a' }} />
                  <span>Upcoming Appointments</span>
                </div>
              }
              extra={<Button type="link" onClick={() => navigate('/patient/appointments')}>View All</Button>}
              style={{ borderRadius: 12, height: '100%' }}
            >
              {appointments.length > 0 ? (
                <div className="space-y-3">
                  {appointments.slice(0, 3).map((apt: any) => (
                    <div key={apt.id} className="p-3 bg-gray-50 rounded">
                      <Text strong>{apt.doctor?.name}</Text>
                      <br />
                      <Text className="text-gray-500 text-sm">
                        {apt.doctor?.specialization} • {apt.date} at {apt.time}
                      </Text>
                      <br />
                      <Text className="text-gray-500 text-sm">{apt.doctor?.hospital}</Text>
                    </div>
                  ))}
                </div>
              ) : (
                <Empty description="No upcoming appointments" image={Empty.PRESENTED_IMAGE_SIMPLE} />
              )}
            </Card>
          </Col>

          {/* Section 4: Family Health */}
          <Col xs={24} md={12}>
            <Card
              title={
                <div className="flex items-center gap-2">
                  <TeamOutlined style={{ color: '#722ed1' }} />
                  <span>Family Health</span>
                </div>
              }
              extra={
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  size="small"
                  onClick={() => navigate('/patient/family')}
                >
                  Add Member
                </Button>
              }
              style={{ borderRadius: 12 }}
            >
              <Empty description="Add family members to manage their health" image={Empty.PRESENTED_IMAGE_SIMPLE}>
                <Button type="link" onClick={() => navigate('/patient/family')}>Manage Family</Button>
              </Empty>
            </Card>
          </Col>

          {/* Section 5: Recent AI Sessions */}
          <Col xs={24} md={12}>
            <Card
              title={
                <div className="flex items-center gap-2">
                  <FileTextOutlined style={{ color: '#13c2c2' }} />
                  <span>Recent AI Sessions</span>
                </div>
              }
              style={{ borderRadius: 12 }}
            >
              {recentSessions.length > 0 ? (
                <div className="space-y-3">
                  {recentSessions.map((session: any) => (
                    <div key={session.id} className="p-3 bg-gray-50 rounded">
                      <div className="flex justify-between items-start mb-2">
                        <Text strong className="text-sm">{session.symptom_input.substring(0, 50)}...</Text>
                        <Tag color={getSeverityColor(session.severity_score)}>
                          {session.severity_score}/10
                        </Tag>
                      </div>
                      <Text className="text-gray-500 text-xs">
                        {session.recommended_specialist} • {new Date(session.created_at).toLocaleDateString()}
                      </Text>
                    </div>
                  ))}
                </div>
              ) : (
                <Empty description="No recent sessions" image={Empty.PRESENTED_IMAGE_SIMPLE} />
              )}
            </Card>
          </Col>
        </Row>

        {/* Follow-up Questions Modal */}
        <Modal
          title="Please Answer These Questions"
          open={showQuestions}
          onCancel={() => setShowQuestions(false)}
          footer={[
            <Button key="back" onClick={() => setShowQuestions(false)}>Cancel</Button>,
            <Button key="submit" type="primary" onClick={handleTriage} loading={loading}>
              Submit Answers
            </Button>
          ]}
          width={600}
        >
          <div className="space-y-4">
            {questions.map((q: any, idx: number) => (
              <div key={q.id} className="p-4 bg-gray-50 rounded">
                <Text strong className="block mb-2">{idx + 1}. {q.question}</Text>
                
                {q.type === 'scale' && (
                  <div>
                    <Input
                      type="number"
                      min={1}
                      max={10}
                      placeholder="1-10"
                      value={answers[q.id] || ''}
                      onChange={(e) => setAnswers({...answers, [q.id]: e.target.value})}
                    />
                  </div>
                )}
                
                {q.type === 'choice' && q.options && (
                  <div className="space-y-2">
                    {q.options.map((opt: string) => (
                      <Button
                        key={opt}
                        block
                        type={answers[q.id] === opt ? 'primary' : 'default'}
                        onClick={() => setAnswers({...answers, [q.id]: opt})}
                      >
                        {opt}
                      </Button>
                    ))}
                  </div>
                )}
                
                {q.type === 'text' && (
                  <TextArea
                    rows={2}
                    placeholder="Your answer..."
                    value={answers[q.id] || ''}
                    onChange={(e) => setAnswers({...answers, [q.id]: e.target.value})}
                  />
                )}
                
                {q.type === 'yes_no' && (
                  <div className="flex gap-2">
                    <Button
                      type={answers[q.id] === 'Yes' ? 'primary' : 'default'}
                      onClick={() => setAnswers({...answers, [q.id]: 'Yes'})}
                      block
                    >
                      Yes
                    </Button>
                    <Button
                      type={answers[q.id] === 'No' ? 'primary' : 'default'}
                      onClick={() => setAnswers({...answers, [q.id]: 'No'})}
                      block
                    >
                      No
                    </Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Modal>

        {/* AI Triage Results Modal */}
        <Modal
          title={result?.is_emergency ? '🚨 EMERGENCY DETECTED' : 'AI Health Assessment'}
          open={!!result}
          onCancel={() => setResult(null)}
          footer={null}
          width={700}
          style={result?.is_emergency ? { border: '3px solid #f5222d' } : {}}
        >
          {result?.is_emergency ? (
            <div className="bg-red-50 p-6 rounded mb-4">
              <Title level={3} className="!text-red-600 !mb-4">IMMEDIATE ACTION REQUIRED</Title>
              <Button
                type="primary"
                danger
                size="large"
                block
                className="!h-16 !text-xl !mb-3"
                onClick={() => window.open('tel:108')}
              >
                📞 Call 108 Ambulance NOW
              </Button>
              {result.nearest_hospital && (
                <div className="mt-4 p-4 bg-white rounded">
                  <Text strong>Nearest Emergency Hospital:</Text>
                  <br />
                  <Text>{result.nearest_hospital.name}</Text>
                  <br />
                  <Text className="text-gray-500">{result.nearest_hospital.distance_km} km away</Text>
                </div>
              )}
            </div>
          ) : (
            <div>
              <div className="mb-6 p-6 bg-blue-50 rounded text-center">
                <div className="mb-2">
                  <Progress
                    type="circle"
                    percent={result?.severity_score * 10}
                    format={() => `${result?.severity_score}/10`}
                    strokeColor={getSeverityColor(result?.severity_score)}
                    size={120}
                  />
                </div>
                <Tag
                  color={getSeverityColor(result?.severity_score)}
                  className="text-lg px-4 py-1"
                >
                  {getSeverityLabel(result?.severity_score)}
                </Tag>
              </div>

              <div className="space-y-4">
                <div>
                  <Text strong className="text-lg">Urgency: </Text>
                  <Text className="text-lg">{result?.urgency}</Text>
                </div>

                <div>
                  <Text strong className="text-lg">Recommended Specialist: </Text>
                  <Text className="text-lg text-blue-600">{result?.recommended_specialist}</Text>
                </div>

                {result?.risk_factors?.length > 0 && (
                  <div>
                    <Text strong>Risk Factors:</Text>
                    <ul className="mt-2">
                      {result.risk_factors.map((factor: string, i: number) => (
                        <li key={i} className="text-gray-700">{factor}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {result?.suggested_tests?.length > 0 && (
                  <div>
                    <Text strong>Suggested Tests:</Text>
                    <ul className="mt-2">
                      {result.suggested_tests.map((test: string, i: number) => (
                        <li key={i} className="text-gray-700">{test}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {result?.differential_diagnoses?.length > 0 && (
                  <div>
                    <Text strong>Possible Conditions:</Text>
                    <ul className="mt-2">
                      {result.differential_diagnoses.map((diagnosis: string, i: number) => (
                        <li key={i} className="text-gray-700">{diagnosis}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="mt-6 flex gap-3">
                  <Button
                    type="primary"
                    size="large"
                    block
                    onClick={() => {
                      setResult(null)
                      navigate(`/patient/doctors?specialization=${encodeURIComponent(result?.recommended_specialist || 'General Physician')}`)
                    }}
                  >
                    Find Doctors Near Me
                  </Button>
                  <Button size="large" onClick={() => setResult(null)}>
                    New Assessment
                  </Button>
                </div>

                <div className="mt-4 p-3 bg-gray-50 rounded">
                  <Text className="text-xs text-gray-500">
                    <strong>Disclaimer:</strong> This is an AI-powered triage assessment and not a medical diagnosis.
                    Please consult a qualified healthcare professional for proper medical advice.
                  </Text>
                </div>
              </div>
            </div>
          )}
        </Modal>
      </div>
    </div>
  )
}

