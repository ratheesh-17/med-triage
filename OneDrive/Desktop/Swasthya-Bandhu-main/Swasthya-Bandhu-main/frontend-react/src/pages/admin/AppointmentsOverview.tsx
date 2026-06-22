import { useState } from 'react'
import { Card, Table, Tag, Row, Col, Typography, DatePicker, Select, Modal, Descriptions } from 'antd'
import { LineChart, Line, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

const APPOINTMENTS_DATA = [
  {
    id: 1,
    patientName: 'Rajesh Kumar',
    doctorName: 'Dr. Meera Sharma',
    specialization: 'Cardiologist',
    date: '2024-01-20',
    time: '10:00 AM',
    type: 'In-Person',
    severity: 9,
    status: 'Completed'
  },
  {
    id: 2,
    patientName: 'Priya Sharma',
    doctorName: 'Dr. Amit Verma',
    specialization: 'Pediatrician',
    date: '2024-01-20',
    time: '11:30 AM',
    type: 'Online',
    severity: 4,
    status: 'Confirmed'
  },
  {
    id: 3,
    patientName: 'Amit Patel',
    doctorName: 'Dr. Sunita Reddy',
    specialization: 'Dermatologist',
    date: '2024-01-19',
    time: '02:00 PM',
    type: 'In-Person',
    severity: 5,
    status: 'Cancelled'
  }
]

const CANCELLATION_TREND = [
  { week: 'Week 1', rate: 5 },
  { week: 'Week 2', rate: 7 },
  { week: 'Week 3', rate: 6 },
  { week: 'Week 4', rate: 8 }
]

const CANCELLATION_REASONS = [
  { reason: 'Doctor unavailable', count: 12 },
  { reason: 'Patient schedule conflict', count: 18 },
  { reason: 'Feeling better', count: 8 },
  { reason: 'Found alternative', count: 5 }
]

export default function AppointmentsOverview() {
  const [selectedAppointment, setSelectedAppointment] = useState<any>(null)
  const [detailModal, setDetailModal] = useState(false)

  const getSeverityColor = (severity: number) => {
    if (severity <= 4) return 'green'
    if (severity <= 6) return 'orange'
    if (severity <= 8) return 'red'
    return 'red'
  }

  const getStatusColor = (status: string) => {
    if (status === 'Completed') return 'green'
    if (status === 'Confirmed') return 'blue'
    return 'red'
  }

  const columns = [
    {
      title: 'Patient',
      dataIndex: 'patientName',
      key: 'patientName'
    },
    {
      title: 'Doctor',
      dataIndex: 'doctorName',
      key: 'doctorName'
    },
    {
      title: 'Specialization',
      dataIndex: 'specialization',
      key: 'specialization'
    },
    {
      title: 'Date & Time',
      key: 'datetime',
      render: (record: any) => (
        <div>
          <Text strong className="block">{record.date}</Text>
          <Text className="text-gray-500 text-sm">{record.time}</Text>
        </div>
      )
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={type === 'Online' ? 'blue' : 'green'}>{type}</Tag>
      )
    },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: number) => (
        <Tag color={getSeverityColor(severity)}>{severity}/10</Tag>
      )
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>{status}</Tag>
      )
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: any, record: any) => (
        <a
          onClick={() => {
            setSelectedAppointment(record)
            setDetailModal(true)
          }}
        >
          View Details
        </a>
      )
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2} className="mb-6">Appointments Overview</Title>

        {/* Summary Cards */}
        <Row gutter={16} className="mb-6">
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">156</Title>
              <Text className="text-gray-500">Total Today</Text>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">892</Title>
              <Text className="text-gray-500">Total This Week</Text>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">3,421</Title>
              <Text className="text-gray-500">Total This Month</Text>
            </Card>
          </Col>
        </Row>

        {/* Filters */}
        <Card className="mb-6 shadow-sm">
          <Row gutter={16}>
            <Col xs={24} sm={12} lg={6}>
              <RangePicker className="w-full" placeholder={['Start Date', 'End Date']} />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Select className="w-full" placeholder="Specialization" allowClear>
                <Select.Option value="cardiologist">Cardiologist</Select.Option>
                <Select.Option value="pediatrician">Pediatrician</Select.Option>
                <Select.Option value="dermatologist">Dermatologist</Select.Option>
              </Select>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Select className="w-full" placeholder="Severity Level" allowClear>
                <Select.Option value="low">Low (1-4)</Select.Option>
                <Select.Option value="moderate">Moderate (5-6)</Select.Option>
                <Select.Option value="high">High (7-8)</Select.Option>
                <Select.Option value="emergency">Emergency (9-10)</Select.Option>
              </Select>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Select className="w-full" placeholder="Status" allowClear>
                <Select.Option value="confirmed">Confirmed</Select.Option>
                <Select.Option value="completed">Completed</Select.Option>
                <Select.Option value="cancelled">Cancelled</Select.Option>
              </Select>
            </Col>
          </Row>
        </Card>

        {/* Appointments Table */}
        <Card className="mb-6 shadow-sm">
          <Table
            columns={columns}
            dataSource={APPOINTMENTS_DATA}
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        </Card>

        {/* Cancellation Analytics */}
        <Row gutter={16}>
          <Col xs={24} lg={12}>
            <Card title="Cancellation Rate Over Time" className="shadow-sm">
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={CANCELLATION_TREND}>
                  <XAxis dataKey="week" />
                  <YAxis />
                  <RechartsTooltip />
                  <Line type="monotone" dataKey="rate" stroke="#f5222d" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card title="Most Common Cancellation Reasons" className="shadow-sm">
              <div className="space-y-3">
                {CANCELLATION_REASONS.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <Text>{item.reason}</Text>
                    <Tag color="red">{item.count} cases</Tag>
                  </div>
                ))}
              </div>
            </Card>
          </Col>
        </Row>

        {/* Appointment Detail Modal */}
        <Modal
          title="Appointment Details"
          open={detailModal}
          onCancel={() => setDetailModal(false)}
          footer={null}
          width={600}
        >
          {selectedAppointment && (
            <Descriptions bordered column={1}>
              <Descriptions.Item label="Appointment ID">{selectedAppointment.id}</Descriptions.Item>
              <Descriptions.Item label="Patient">{selectedAppointment.patientName}</Descriptions.Item>
              <Descriptions.Item label="Doctor">{selectedAppointment.doctorName}</Descriptions.Item>
              <Descriptions.Item label="Specialization">{selectedAppointment.specialization}</Descriptions.Item>
              <Descriptions.Item label="Date">{selectedAppointment.date}</Descriptions.Item>
              <Descriptions.Item label="Time">{selectedAppointment.time}</Descriptions.Item>
              <Descriptions.Item label="Consultation Type">
                <Tag color={selectedAppointment.type === 'Online' ? 'blue' : 'green'}>
                  {selectedAppointment.type}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="AI Severity Score">
                <Tag color={getSeverityColor(selectedAppointment.severity)}>
                  {selectedAppointment.severity}/10
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Status">
                <Tag color={getStatusColor(selectedAppointment.status)}>
                  {selectedAppointment.status}
                </Tag>
              </Descriptions.Item>
            </Descriptions>
          )}
        </Modal>
      </div>
    </div>
  )
}
