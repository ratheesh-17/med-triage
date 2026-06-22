import { Card, Tag, Button, Typography, Row, Col, Input } from 'antd'
import { WarningOutlined, LineChartOutlined } from '@ant-design/icons'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input

const CLUSTER_DATA = {
  region: 'Coimbatore',
  alertLevel: 'Alert',
  detectedDate: '2024-01-20',
  totalCases: 23,
  symptoms: [
    { symptom: 'Fever', frequency: 23 },
    { symptom: 'Cough', frequency: 21 },
    { symptom: 'Fatigue', frequency: 18 },
    { symptom: 'Body ache', frequency: 15 }
  ],
  timeline: [
    { date: 'Jan 14', cases: 2 },
    { date: 'Jan 15', cases: 3 },
    { date: 'Jan 16', cases: 4 },
    { date: 'Jan 17', cases: 5 },
    { date: 'Jan 18', cases: 6 },
    { date: 'Jan 19', cases: 7 },
    { date: 'Jan 20', cases: 8 }
  ]
}

export default function OutbreakDetail() {

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <Title level={2}>Outbreak Detection Detail</Title>
          <Text className="text-gray-500">Region: {CLUSTER_DATA.region}</Text>
        </div>

        {/* Alert Banner */}
        <Card className="mb-6 shadow-sm border-red-500 bg-red-50">
          <div className="flex items-start gap-4">
            <WarningOutlined style={{ fontSize: 48, color: '#f5222d' }} />
            <div className="flex-1">
              <Title level={3} className="!mb-2 text-red-600">Potential Outbreak Detected</Title>
              <Paragraph className="!mb-2">
                <Text strong>Region:</Text> {CLUSTER_DATA.region}<br />
                <Text strong>Alert Level:</Text> <Tag color="red">{CLUSTER_DATA.alertLevel}</Tag><br />
                <Text strong>First Detected:</Text> {CLUSTER_DATA.detectedDate}<br />
                <Text strong>Total Cases:</Text> {CLUSTER_DATA.totalCases} cases in last 7 days
              </Paragraph>
            </div>
          </div>
        </Card>

        <Row gutter={[16, 16]} className="mb-6">
          {/* Symptom Breakdown */}
          <Col xs={24} lg={12}>
            <Card title="Symptom Breakdown" className="shadow-sm">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={CLUSTER_DATA.symptoms}>
                  <XAxis dataKey="symptom" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="frequency" fill="#f5222d" />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-yellow-50 rounded">
                <Text strong>Common Pattern:</Text>
                <Paragraph className="!mb-0 mt-2">
                  Fever + Cough + Fatigue appearing together in {Math.round((18/23)*100)}% of cases
                </Paragraph>
              </div>
            </Card>
          </Col>

          {/* Timeline */}
          <Col xs={24} lg={12}>
            <Card title="Case Count Timeline (Last 14 Days)" className="shadow-sm">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={CLUSTER_DATA.timeline}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="cases" stroke="#f5222d" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-red-50 rounded">
                <LineChartOutlined className="text-red-600 mr-2" />
                <Text strong className="text-red-600">Trend: Growing</Text>
                <Paragraph className="!mb-0 mt-2">
                  Case count has increased by 300% over the last 7 days
                </Paragraph>
              </div>
            </Card>
          </Col>
        </Row>

        {/* Admin Notes */}
        <Card title="Admin Observations" className="mb-6 shadow-sm">
          <TextArea
            rows={4}
            placeholder="Add your observations about this cluster..."
            defaultValue="Monitoring closely. Pattern suggests viral respiratory infection. Recommend continued surveillance."
          />
          <Button type="primary" className="mt-3">Save Notes</Button>
        </Card>

        {/* Escalation */}
        <Card className="shadow-sm bg-blue-50 border-blue-300">
          <div className="flex items-center justify-between">
            <div>
              <Title level={4} className="!mb-2">Escalate to Health Authority</Title>
              <Paragraph className="!mb-0">
                Send this cluster report to local health authorities for investigation and intervention.
                This feature will be available in production.
              </Paragraph>
            </div>
            <Button type="primary" size="large" disabled>
              Coming Soon
            </Button>
          </div>
        </Card>
      </div>
    </div>
  )
}
