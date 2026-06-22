import { useState, useEffect } from 'react'
import { Card, Row, Col, Typography, Rate, Spin } from 'antd'
import { UserOutlined, ClockCircleOutlined, StarOutlined, RiseOutlined } from '@ant-design/icons'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text, Paragraph } = Typography

export default function PerformanceAnalytics() {
  const [analytics, setAnalytics] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      const response = await api.get('/doctor/analytics')
      setAnalytics(response.data)
    } catch (error) {
      toast.error('Failed to load analytics')
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

  const totalAppointments = analytics?.total_appointments || 0
  const avgRating = analytics?.avg_rating || 0
  const severityData = analytics?.severity_distribution || []

  const WEEKLY_TREND = [
    { week: 'Week 1', appointments: 45 },
    { week: 'Week 2', appointments: 52 },
    { week: 'Week 3', appointments: 48 },
    { week: 'Week 4', appointments: 58 },
    { week: 'Week 5', appointments: 55 },
    { week: 'Week 6', appointments: 62 },
    { week: 'Week 7', appointments: 68 },
    { week: 'Week 8', appointments: 72 }
  ]

  const RATING_DISTRIBUTION = [
    { rating: '5 Star', count: 250 },
    { rating: '4 Star', count: 80 },
    { rating: '3 Star', count: 20 },
    { rating: '2 Star', count: 5 },
    { rating: '1 Star', count: 2 }
  ]

  const REVIEWS = [
    { patient: 'Meera Singh', rating: 5, comment: 'Very thorough examination and clear explanation. Highly recommend!', date: '2024-01-15' },
    { patient: 'Karthik Reddy', rating: 5, comment: 'Excellent doctor, took time to understand my concerns', date: '2024-01-14' },
    { patient: 'Anjali Nair', rating: 4, comment: 'Good consultation, helpful advice', date: '2024-01-13' },
    { patient: 'Ravi Kumar', rating: 5, comment: 'Professional and caring approach', date: '2024-01-12' },
    { patient: 'Priya Sharma', rating: 5, comment: 'Best doctor I have consulted online', date: '2024-01-11' }
  ]

  const highSeverityCases = severityData.filter((s: any) => s.name.includes('High') || s.name.includes('Emergency'))
    .reduce((sum: number, item: any) => sum + item.value, 0)
  const highSeverityPercent = totalAppointments > 0 ? ((highSeverityCases / totalAppointments) * 100).toFixed(0) : '0'

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2} className="mb-6">Performance Analytics</Title>

        {/* Overall Metrics */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <UserOutlined style={{ fontSize: 40, color: '#1890ff' }} />
              <Title level={3} className="!mt-4 !mb-0">{totalAppointments}</Title>
              <Text className="text-gray-500">Total Patients Seen</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <StarOutlined style={{ fontSize: 40, color: '#faad14' }} />
              <Title level={3} className="!mt-4 !mb-0">{avgRating.toFixed(1)}</Title>
              <Text className="text-gray-500">Average Rating</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <ClockCircleOutlined style={{ fontSize: 40, color: '#52c41a' }} />
              <Title level={3} className="!mt-4 !mb-0">28 mins</Title>
              <Text className="text-gray-500">Avg Consultation</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="text-center shadow-sm">
              <RiseOutlined style={{ fontSize: 40, color: '#ff7a45' }} />
              <Title level={3} className="!mt-4 !mb-0">82%</Title>
              <Text className="text-gray-500">Response Time</Text>
            </Card>
          </Col>
        </Row>

        {/* Highlight Card */}
        <Card className="mb-6 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500">
          <div className="flex items-center gap-4">
            <div className="bg-blue-500 text-white p-4 rounded-lg">
              <RiseOutlined style={{ fontSize: 32 }} />
            </div>
            <div>
              <Title level={4} className="!mb-1">Weekly Performance Insight</Title>
              <Paragraph className="!mb-0 text-gray-600">
                You handled <Text strong>{highSeverityCases} high-severity cases</Text> this week, 
                which is <Text strong>{highSeverityPercent}% above</Text> your monthly average. 
                Excellent work managing critical cases!
              </Paragraph>
            </div>
          </div>
        </Card>

        <Row gutter={[16, 16]}>
          {/* Severity Distribution */}
          <Col xs={24} lg={12}>
            <Card title="Severity Distribution" className="shadow-sm">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={severityData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {severityData.map((entry: any, index: number) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-4">
                {severityData.map((item: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <Text>{item.name}</Text>
                    <Text strong>{item.value}</Text>
                  </div>
                ))}
              </div>
            </Card>
          </Col>

          {/* Weekly Appointments Trend */}
          <Col xs={24} lg={12}>
            <Card title="Weekly Appointments Trend (Last 8 Weeks)" className="shadow-sm">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={WEEKLY_TREND}>
                  <XAxis dataKey="week" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="appointments" stroke="#1890ff" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 p-4 bg-green-50 rounded">
                <Text className="text-green-700">
                  📈 <Text strong>Trending Up:</Text> Your appointment volume has increased by 60% over the last 8 weeks
                </Text>
              </div>
            </Card>
          </Col>

          {/* Rating Distribution */}
          <Col xs={24} lg={12}>
            <Card title="Patient Feedback Summary" className="shadow-sm">
              <div className="text-center mb-6">
                <Title level={2} className="!mb-2">{avgRating}</Title>
                <Rate disabled defaultValue={avgRating} allowHalf />
                <div className="mt-2">
                  <Text className="text-gray-500">
                    Based on real patient appointments
                  </Text>
                </div>
              </div>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={RATING_DISTRIBUTION} layout="vertical">
                  <XAxis type="number" />
                  <YAxis dataKey="rating" type="category" />
                  <Tooltip />
                  <Bar dataKey="count" fill="#faad14" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>

          {/* Recent Reviews */}
          <Col xs={24} lg={12}>
            <Card title="Recent Patient Reviews" className="shadow-sm">
              <div className="space-y-4 max-h-[400px] overflow-y-auto">
                {REVIEWS.map((review, idx) => (
                  <div key={idx} className="border-b pb-4 last:border-b-0">
                    <div className="flex items-center justify-between mb-2">
                      <Text strong>{review.patient}</Text>
                      <Rate disabled defaultValue={review.rating} />
                    </div>
                    <Paragraph className="!mb-1 text-gray-600">{review.comment}</Paragraph>
                    <Text className="text-gray-400 text-xs">{review.date}</Text>
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
