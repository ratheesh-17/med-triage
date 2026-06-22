import { Card, Row, Col, Badge, Button, Typography, Alert, Table, Tag, Spin } from 'antd'
import { UserOutlined, MedicineBoxOutlined, CalendarOutlined, WarningOutlined, BellOutlined } from '@ant-design/icons'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../../services/api'

const { Title, Text } = Typography

export default function AdminDashboard() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [metrics, setMetrics] = useState<any>(null)
  const [outbreaks, setOutbreaks] = useState<any[]>([])

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await api.get('/admin/analytics')
      setMetrics(response.data.analytics)
      setOutbreaks(response.data.outbreak_alerts || [])
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Spin size="large" />
      </div>
    )
  }

  if (!metrics) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <Alert message="Failed to load dashboard data" type="error" />
      </div>
    )
  }

  const platformMetrics = metrics.platform_metrics
  const hasAlert = outbreaks.some((o: any) => o.severity === 'high')

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <Title level={2}>Admin Dashboard</Title>
            <Badge count="Admin Panel" style={{ backgroundColor: '#1890ff' }} />
          </div>
          <Badge count={platformMetrics.pending_verifications} offset={[-5, 5]}>
            <BellOutlined style={{ fontSize: 24, color: '#faad14' }} />
          </Badge>
        </div>

        {/* Platform Overview */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm">
              <UserOutlined style={{ fontSize: 32, color: '#1890ff' }} />
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.total_patients}</Title>
              <Text className="text-gray-500">Total Patients</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm">
              <MedicineBoxOutlined style={{ fontSize: 32, color: '#52c41a' }} />
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.total_doctors}</Title>
              <Text className="text-gray-500">Verified Doctors</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm">
              <CalendarOutlined style={{ fontSize: 32, color: '#faad14' }} />
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.appointments_today}</Title>
              <Text className="text-gray-500">Appointments Today</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm">
              <CalendarOutlined style={{ fontSize: 32, color: '#722ed1' }} />
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.appointments_month}</Title>
              <Text className="text-gray-500">This Month</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm border-orange-300">
              <Badge count={platformMetrics.pending_verifications} style={{ backgroundColor: '#faad14' }}>
                <WarningOutlined style={{ fontSize: 32, color: '#faad14' }} />
              </Badge>
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.pending_verifications}</Title>
              <Text className="text-gray-500">Pending Verifications</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={4}>
            <Card className="text-center shadow-sm border-red-300">
              <Badge count={platformMetrics.emergency_cases} style={{ backgroundColor: '#f5222d' }}>
                <WarningOutlined style={{ fontSize: 32, color: '#f5222d' }} />
              </Badge>
              <Title level={3} className="!mt-4 !mb-0">{platformMetrics.emergency_cases}</Title>
              <Text className="text-gray-500">Emergency Cases (24h)</Text>
            </Card>
          </Col>
        </Row>

        {/* Pending Verifications Alert */}
        {platformMetrics.pending_verifications > 0 ? (
          <Alert
            message={`${platformMetrics.pending_verifications} doctors awaiting verification`}
            type="warning"
            showIcon
            action={
              <Button type="primary" size="small" onClick={() => navigate('/admin/doctor-verification')}>
                Review Now
              </Button>
            }
            className="mb-6"
          />
        ) : (
          <Alert message="All doctors verified" type="success" showIcon className="mb-6" />
        )}

        {/* Platform Analytics */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24} lg={12}>
            <Card title="Urgency Distribution (All AI Sessions)" className="shadow-sm">
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={metrics.urgency_distribution} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                    {metrics.urgency_distribution.map((entry: any, index: number) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="Specialist Demand Ranking" className="shadow-sm">
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={metrics.specialist_demand} layout="vertical">
                  <XAxis type="number" />
                  <YAxis dataKey="specialization" type="category" width={120} />
                  <RechartsTooltip />
                  <Bar dataKey="count" fill="#722ed1" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>

        {/* Symptom Intelligence */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24}>
            <Card title="Top 10 Most Reported Symptoms" className="shadow-sm">
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={metrics.top_symptoms} layout="vertical">
                  <XAxis type="number" />
                  <YAxis dataKey="symptom" type="category" width={100} />
                  <RechartsTooltip />
                  <Bar dataKey="count" fill="#1890ff" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>

        {/* Outbreak Detection Monitor */}
        {outbreaks.length > 0 && (
          <Card title="Outbreak Detection Monitor" className="mb-6 shadow-sm">
            {hasAlert && (
              <Alert
                message="⚠️ Potential Outbreak Detected"
                description={`${outbreaks[0].region}: ${outbreaks[0].case_count} cases detected`}
                type="error"
                showIcon
                className="mb-4"
              />
            )}
            <Table
              dataSource={outbreaks.map((o: any, idx: number) => ({ ...o, key: idx }))}
              columns={[
                { title: 'Region', dataIndex: 'region', key: 'region' },
                { title: 'Cases (7 days)', dataIndex: 'case_count', key: 'case_count' },
                { title: 'Symptom Cluster', dataIndex: 'symptom_cluster', key: 'symptom_cluster', render: (val: any) => Array.isArray(val) ? val.join(', ') : val },
                {
                  title: 'Severity',
                  dataIndex: 'severity',
                  key: 'severity',
                  render: (severity: string) => (
                    <Tag color={severity === 'high' ? 'red' : 'orange'}>{severity.toUpperCase()}</Tag>
                  )
                }
              ]}
              pagination={false}
              size="small"
            />
          </Card>
        )}
      </div>
    </div>
  )
}
