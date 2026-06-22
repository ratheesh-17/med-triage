import { useState } from 'react'
import { Card, Table, Input, Button, Drawer, Descriptions, Tag, Modal, Typography, Row, Col, DatePicker, Select, message } from 'antd'
import { SearchOutlined, ExportOutlined, UserOutlined, StopOutlined } from '@ant-design/icons'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

const PATIENTS_DATA = [
  {
    id: 1,
    name: 'Rajesh Kumar',
    phone: '+91 9876543210',
    registrationDate: '2024-01-10',
    aiSessions: 5,
    appointments: 3,
    status: 'Active',
    healthRisk: { cardiac: 65, metabolic: 40, neurological: 30 },
    family: 2
  },
  {
    id: 2,
    name: 'Priya Sharma',
    phone: '+91 9876543211',
    registrationDate: '2024-01-12',
    aiSessions: 3,
    appointments: 2,
    status: 'Active',
    healthRisk: { cardiac: 30, metabolic: 45, neurological: 25 },
    family: 1
  },
  {
    id: 3,
    name: 'Amit Patel',
    phone: '+91 9876543212',
    registrationDate: '2024-01-08',
    aiSessions: 8,
    appointments: 5,
    status: 'Active',
    healthRisk: { cardiac: 75, metabolic: 60, neurological: 40 },
    family: 3
  }
]

export default function PatientManagement() {
  const [searchText, setSearchText] = useState('')
  const [selectedPatient, setSelectedPatient] = useState<any>(null)
  const [drawerVisible, setDrawerVisible] = useState(false)
  const [deactivateModal, setDeactivateModal] = useState(false)
  const [deactivateReason, setDeactivateReason] = useState('')

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      filteredValue: [searchText],
      onFilter: (value: any, record: any) =>
        record.name.toLowerCase().includes(value.toLowerCase()) ||
        record.phone.includes(value)
    },
    {
      title: 'Phone',
      dataIndex: 'phone',
      key: 'phone'
    },
    {
      title: 'Registration Date',
      dataIndex: 'registrationDate',
      key: 'registrationDate'
    },
    {
      title: 'AI Sessions',
      dataIndex: 'aiSessions',
      key: 'aiSessions',
      align: 'center' as const
    },
    {
      title: 'Appointments',
      dataIndex: 'appointments',
      key: 'appointments',
      align: 'center' as const
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Active' ? 'green' : 'red'}>{status}</Tag>
      )
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: any, record: any) => (
        <Button
          size="small"
          onClick={() => {
            setSelectedPatient(record)
            setDrawerVisible(true)
          }}
        >
          View Details
        </Button>
      )
    }
  ]

  const handleDeactivate = () => {
    if (!deactivateReason.trim()) {
      message.error('Please provide a reason for deactivation')
      return
    }
    message.success(`Patient account deactivated. Reason logged in audit.`)
    setDeactivateModal(false)
    setDeactivateReason('')
    setDrawerVisible(false)
  }

  const handleExport = () => {
    message.success('Patient list exported as CSV')
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Title level={2}>Patient Management</Title>
          <Button icon={<ExportOutlined />} onClick={handleExport}>
            Export CSV
          </Button>
        </div>

        <Card className="mb-6 shadow-sm">
          <Row gutter={16}>
            <Col xs={24} sm={12} lg={8}>
              <Input
                placeholder="Search by name or phone"
                prefix={<SearchOutlined />}
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                allowClear
              />
            </Col>
            <Col xs={24} sm={12} lg={8}>
              <RangePicker className="w-full" placeholder={['Start Date', 'End Date']} />
            </Col>
            <Col xs={24} sm={12} lg={8}>
              <Select className="w-full" placeholder="Account Status" allowClear>
                <Select.Option value="active">Active</Select.Option>
                <Select.Option value="deactivated">Deactivated</Select.Option>
              </Select>
            </Col>
          </Row>
        </Card>

        <Card className="shadow-sm">
          <Table
            columns={columns}
            dataSource={PATIENTS_DATA}
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        </Card>

        {/* Patient Detail Drawer */}
        <Drawer
          title="Patient Details"
          placement="right"
          width={600}
          open={drawerVisible}
          onClose={() => setDrawerVisible(false)}
        >
          {selectedPatient && (
            <div>
              <div className="text-center mb-6">
                <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                  <UserOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                </div>
                <Title level={4} className="!mb-1">{selectedPatient.name}</Title>
                <Text className="text-gray-500">{selectedPatient.phone}</Text>
              </div>

              <Descriptions bordered column={1} size="small" className="mb-6">
                <Descriptions.Item label="Patient ID">{selectedPatient.id}</Descriptions.Item>
                <Descriptions.Item label="Registration Date">{selectedPatient.registrationDate}</Descriptions.Item>
                <Descriptions.Item label="Total AI Sessions">{selectedPatient.aiSessions}</Descriptions.Item>
                <Descriptions.Item label="Total Appointments">{selectedPatient.appointments}</Descriptions.Item>
                <Descriptions.Item label="Family Members">{selectedPatient.family}</Descriptions.Item>
                <Descriptions.Item label="Account Status">
                  <Tag color={selectedPatient.status === 'Active' ? 'green' : 'red'}>
                    {selectedPatient.status}
                  </Tag>
                </Descriptions.Item>
              </Descriptions>

              <Card title="Health Risk Index" size="small" className="mb-6">
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between mb-1">
                      <Text>Cardiac Risk</Text>
                      <Text strong>{selectedPatient.healthRisk.cardiac}%</Text>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full"
                        style={{ width: `${selectedPatient.healthRisk.cardiac}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <Text>Metabolic Risk</Text>
                      <Text strong>{selectedPatient.healthRisk.metabolic}%</Text>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full"
                        style={{ width: `${selectedPatient.healthRisk.metabolic}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <Text>Neurological Risk</Text>
                      <Text strong>{selectedPatient.healthRisk.neurological}%</Text>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-yellow-500 h-2 rounded-full"
                        style={{ width: `${selectedPatient.healthRisk.neurological}%` }}
                      />
                    </div>
                  </div>
                </div>
              </Card>

              <Button
                danger
                block
                icon={<StopOutlined />}
                onClick={() => setDeactivateModal(true)}
              >
                Deactivate Account
              </Button>
            </div>
          )}
        </Drawer>

        {/* Deactivate Modal */}
        <Modal
          title="Deactivate Patient Account"
          open={deactivateModal}
          onCancel={() => setDeactivateModal(false)}
          onOk={handleDeactivate}
          okText="Confirm Deactivation"
          okButtonProps={{ danger: true }}
        >
          <Text strong className="block mb-2">Patient: {selectedPatient?.name}</Text>
          <Text className="block mb-4">
            Deactivated accounts cannot log in. Please provide a reason (will be logged in audit):
          </Text>
          <Input.TextArea
            rows={4}
            value={deactivateReason}
            onChange={(e) => setDeactivateReason(e.target.value)}
            placeholder="e.g., Suspicious activity, User request, Policy violation, etc."
          />
        </Modal>
      </div>
    </div>
  )
}
