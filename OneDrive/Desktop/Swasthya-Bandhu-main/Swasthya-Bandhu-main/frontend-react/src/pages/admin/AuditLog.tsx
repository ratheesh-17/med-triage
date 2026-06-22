import { Card, Table, Tag, Input, Select, DatePicker, Typography } from 'antd'
import { SearchOutlined } from '@ant-design/icons'

const { Title } = Typography
const { RangePicker } = DatePicker

const AUDIT_DATA = [
  {
    id: 1,
    timestamp: '2024-01-20 14:35:22',
    category: 'Doctor Management',
    action: 'Doctor Approved',
    description: 'Dr. Meera Sharma (Cardiologist) approved',
    userId: 'DOC-1234',
    ipAddress: '192.168.1.100'
  },
  {
    id: 2,
    timestamp: '2024-01-20 14:20:15',
    category: 'Emergency',
    action: 'Emergency Case Flagged',
    description: 'Patient ID: 5678 - Severity 10 - Chest pain',
    userId: 'PAT-5678',
    ipAddress: '192.168.1.105'
  },
  {
    id: 3,
    timestamp: '2024-01-20 13:45:30',
    category: 'Doctor Management',
    action: 'Doctor Rejected',
    description: 'Dr. Amit Kumar - Invalid Medical Council Number',
    userId: 'DOC-5678',
    ipAddress: '192.168.1.102'
  },
  {
    id: 4,
    timestamp: '2024-01-20 12:30:45',
    category: 'Account Management',
    action: 'Account Deactivated',
    description: 'Patient ID: 9012 - Suspicious activity detected',
    userId: 'PAT-9012',
    ipAddress: '192.168.1.108'
  },
  {
    id: 5,
    timestamp: '2024-01-20 11:15:20',
    category: 'Authentication',
    action: 'Admin Login',
    description: 'Admin logged in successfully',
    userId: 'ADMIN',
    ipAddress: '192.168.1.1'
  },
  {
    id: 6,
    timestamp: '2024-01-20 10:50:10',
    category: 'Doctor Management',
    action: 'Doctor Profile Updated',
    description: 'Dr. Priya Sharma updated consultation fees',
    userId: 'DOC-2345',
    ipAddress: '192.168.1.103'
  },
  {
    id: 7,
    timestamp: '2024-01-20 09:30:55',
    category: 'Emergency',
    action: 'Emergency Case Flagged',
    description: 'Patient ID: 3456 - Severity 9 - Severe headache',
    userId: 'PAT-3456',
    ipAddress: '192.168.1.106'
  },
  {
    id: 8,
    timestamp: '2024-01-19 18:20:40',
    category: 'Account Management',
    action: 'Account Reactivated',
    description: 'Patient ID: 7890 - Account restored after review',
    userId: 'PAT-7890',
    ipAddress: '192.168.1.109'
  }
]

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    'Authentication': 'blue',
    'Doctor Management': 'green',
    'Account Management': 'orange',
    'Emergency': 'red'
  }
  return colors[category] || 'default'
}

export default function AuditLog() {
  const columns = [
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 180
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => (
        <Tag color={getCategoryColor(category)}>{category}</Tag>
      )
    },
    {
      title: 'Action',
      dataIndex: 'action',
      key: 'action'
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: 'User/Doctor ID',
      dataIndex: 'userId',
      key: 'userId'
    },
    {
      title: 'IP Address',
      dataIndex: 'ipAddress',
      key: 'ipAddress'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2} className="mb-6">Audit Log</Title>

        <Card className="mb-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Input
              placeholder="Search by action or user ID"
              prefix={<SearchOutlined />}
              allowClear
            />
            <Select placeholder="Category" allowClear className="w-full">
              <Select.Option value="authentication">Authentication</Select.Option>
              <Select.Option value="doctor">Doctor Management</Select.Option>
              <Select.Option value="account">Account Management</Select.Option>
              <Select.Option value="emergency">Emergency</Select.Option>
            </Select>
            <RangePicker className="w-full" />
            <Input placeholder="User ID" allowClear />
          </div>
        </Card>

        <Card className="shadow-sm">
          <Table
            columns={columns}
            dataSource={AUDIT_DATA}
            rowKey="id"
            pagination={{ pageSize: 20 }}
          />
        </Card>

        <Card className="mt-6 shadow-sm bg-blue-50 border-blue-300">
          <p className="text-sm text-gray-700 mb-0">
            <strong>Security Note:</strong> All critical actions on the platform are logged with timestamp, user identification, and IP address for audit trail and compliance purposes. Logs are retained for 90 days.
          </p>
        </Card>
      </div>
    </div>
  )
}
