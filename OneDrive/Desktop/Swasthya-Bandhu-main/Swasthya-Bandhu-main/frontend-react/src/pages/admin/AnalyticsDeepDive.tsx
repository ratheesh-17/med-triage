import { Card, Tabs, Typography, Row, Col, Table, DatePicker } from 'antd'
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const { Title } = Typography
const { RangePicker } = DatePicker

const AGE_DISTRIBUTION = [
  { range: '0-18', value: 15 },
  { range: '19-35', value: 35 },
  { range: '36-50', value: 30 },
  { range: '51-65', value: 15 },
  { range: '65+', value: 5 }
]

const GENDER_DISTRIBUTION = [
  { name: 'Male', value: 52, color: '#1890ff' },
  { name: 'Female', value: 45, color: '#ff7a45' },
  { name: 'Other', value: 3, color: '#52c41a' }
]

const GEOGRAPHIC_DISTRIBUTION = [
  { city: 'Coimbatore', users: 342 },
  { city: 'Chennai', users: 298 },
  { city: 'Bangalore', users: 256 },
  { city: 'Mumbai', users: 189 },
  { city: 'Delhi', users: 162 }
]

const SYMPTOM_TRENDS = [
  { symptom: 'Fever', weekChange: '+23%', trend: 'up' },
  { symptom: 'Cough', weekChange: '+18%', trend: 'up' },
  { symptom: 'Headache', weekChange: '-5%', trend: 'down' },
  { symptom: 'Fatigue', weekChange: '+12%', trend: 'up' }
]

const DOCTOR_PERFORMANCE = [
  { name: 'Dr. Meera Sharma', appointments: 145, rating: 4.8, avgSeverity: 6.2, responseTime: '12 mins' },
  { name: 'Dr. Rajesh Kumar', appointments: 132, rating: 4.7, avgSeverity: 7.1, responseTime: '15 mins' },
  { name: 'Dr. Priya Verma', appointments: 118, rating: 4.9, avgSeverity: 5.8, responseTime: '10 mins' }
]

const API_RESPONSE_TIMES = [
  { time: '00:00', ms: 120 },
  { time: '06:00', ms: 110 },
  { time: '12:00', ms: 180 },
  { time: '18:00', ms: 150 },
  { time: '23:00', ms: 130 }
]

export default function AnalyticsDeepDive() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Title level={2}>Analytics Deep Dive</Title>
          <RangePicker />
        </div>

        <Tabs defaultActiveKey="patient">
          {/* Patient Insights */}
          <Tabs.TabPane tab="Patient Insights" key="patient">
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Age Distribution" className="shadow-sm">
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie data={AGE_DISTRIBUTION} dataKey="value" nameKey="range" cx="50%" cy="50%" outerRadius={80} label>
                        {AGE_DISTRIBUTION.map((_, index) => (
                          <Cell key={index} fill={['#1890ff', '#52c41a', '#faad14', '#ff7a45', '#f5222d'][index]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24} lg={12}>
                <Card title="Gender Distribution" className="shadow-sm">
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie data={GENDER_DISTRIBUTION} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                        {GENDER_DISTRIBUTION.map((entry, index) => (
                          <Cell key={index} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24}>
                <Card title="Geographic Distribution" className="shadow-sm">
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={GEOGRAPHIC_DISTRIBUTION}>
                      <XAxis dataKey="city" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="users" fill="#1890ff" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
            </Row>
          </Tabs.TabPane>

          {/* Health Intelligence */}
          <Tabs.TabPane tab="Health Intelligence" key="health">
            <Row gutter={[16, 16]}>
              <Col xs={24}>
                <Card title="Symptom Trend Analysis (Week-over-Week)" className="shadow-sm">
                  <Table
                    dataSource={SYMPTOM_TRENDS}
                    columns={[
                      { title: 'Symptom', dataIndex: 'symptom', key: 'symptom' },
                      { title: 'Week Change', dataIndex: 'weekChange', key: 'weekChange' },
                      {
                        title: 'Trend',
                        dataIndex: 'trend',
                        key: 'trend',
                        render: (trend) => (
                          <span style={{ color: trend === 'up' ? '#f5222d' : '#52c41a' }}>
                            {trend === 'up' ? '↑ Increasing' : '↓ Decreasing'}
                          </span>
                        )
                      }
                    ]}
                    pagination={false}
                  />
                </Card>
              </Col>
            </Row>
          </Tabs.TabPane>

          {/* Doctor Performance */}
          <Tabs.TabPane tab="Doctor Performance" key="doctor">
            <Card title="Top Performing Doctors" className="shadow-sm">
              <Table
                dataSource={DOCTOR_PERFORMANCE}
                columns={[
                  { title: 'Doctor Name', dataIndex: 'name', key: 'name' },
                  { title: 'Total Appointments', dataIndex: 'appointments', key: 'appointments', align: 'center' },
                  { title: 'Avg Rating', dataIndex: 'rating', key: 'rating', align: 'center' },
                  { title: 'Avg Severity Handled', dataIndex: 'avgSeverity', key: 'avgSeverity', align: 'center' },
                  { title: 'Response Time', dataIndex: 'responseTime', key: 'responseTime', align: 'center' }
                ]}
                pagination={false}
              />
            </Card>
          </Tabs.TabPane>

          {/* Platform Health */}
          <Tabs.TabPane tab="Platform Health" key="platform">
            <Row gutter={[16, 16]}>
              <Col xs={24}>
                <Card title="API Response Times (24 hours)" className="shadow-sm">
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={API_RESPONSE_TIMES}>
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="ms" stroke="#1890ff" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card className="text-center shadow-sm">
                  <Title level={3} className="!mb-0">2,456</Title>
                  <p className="text-gray-500">AI Sessions Today</p>
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card className="text-center shadow-sm">
                  <Title level={3} className="!mb-0">892</Title>
                  <p className="text-gray-500">PDF Reports Generated</p>
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card className="text-center shadow-sm">
                  <Title level={3} className="!mb-0">0.02%</Title>
                  <p className="text-gray-500">Error Rate</p>
                </Card>
              </Col>
            </Row>
          </Tabs.TabPane>
        </Tabs>
      </div>
    </div>
  )
}
