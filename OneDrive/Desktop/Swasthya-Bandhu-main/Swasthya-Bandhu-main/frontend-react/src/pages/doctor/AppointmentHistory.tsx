import { useState, useEffect } from 'react'
import { Card, Table, Tag, DatePicker, Select, Row, Col, Typography, Button, Spin } from 'antd'
import { FilterOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

export default function AppointmentHistory() {
  const [appointments, setAppointments] = useState<any[]>([])
  const [filteredData, setFilteredData] = useState<any[]>([])
  const [severityFilter, setSeverityFilter] = useState<string>('')
  const [typeFilter, setTypeFilter] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAppointments()
  }, [])

  const loadAppointments = async () => {
    try {
      const response = await api.get('/appointments')
      const apts = response.data.appointments || []
      setAppointments(apts)
      setFilteredData(apts)
    } catch (error) {
      toast.error('Failed to load appointments')
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: number) => {
    if (severity <= 4) return 'green'
    if (severity <= 6) return 'orange'
    if (severity <= 8) return 'red'
    return 'red'
  }

  const getSeverityRange = (severity: number) => {
    if (severity <= 4) return 'Low (1-4)'
    if (severity <= 6) return 'Moderate (5-6)'
    if (severity <= 8) return 'High (7-8)'
    return 'Emergency (9-10)'
  }

  const handleFilter = () => {
    let filtered = appointments
    
    if (severityFilter) {
      filtered = filtered.filter(apt => {
        const severity = apt.pre_consult_summary?.severity_score || 0
        if (severityFilter === 'low') return severity <= 4
        if (severityFilter === 'moderate') return severity >= 5 && severity <= 6
        if (severityFilter === 'high') return severity >= 7 && severity <= 8
        if (severityFilter === 'emergency') return severity >= 9
        return true
      })
    }
    
    if (typeFilter) {
      filtered = filtered.filter(apt => apt.slot_type === typeFilter)
    }
    
    setFilteredData(filtered)
  }

  const columns = [
    {
      title: 'Date & Time',
      key: 'datetime',
      render: (record: any) => (
        <div>
          <Text strong className="block">{dayjs(record.date).format('DD MMM YYYY')}</Text>
          <Text className="text-gray-500 text-sm">{record.time}</Text>
        </div>
      )
    },
    {
      title: 'Patient',
      key: 'patient',
      render: (record: any) => (
        <div>
          <Text strong className="block">{record.patient?.name || 'N/A'}</Text>
          <Text className="text-gray-500 text-sm">{record.patient?.age || 0} years</Text>
        </div>
      )
    },
    {
      title: 'Symptoms',
      key: 'symptoms',
      render: (record: any) => record.symptom_notes || 'Not specified',
      ellipsis: true
    },
    {
      title: 'Severity',
      key: 'severity',
      render: (record: any) => {
        const severity = record.pre_consult_summary?.severity_score || 0
        return (
          <Tag color={getSeverityColor(severity)}>
            {severity}/10 - {getSeverityRange(severity)}
          </Tag>
        )
      }
    },
    {
      title: 'Type',
      key: 'type',
      render: (record: any) => (
        <Tag color={record.slot_type === 'online' ? 'blue' : 'green'}>
          {record.slot_type === 'online' ? 'Online' : 'In-Person'}
        </Tag>
      )
    },
    {
      title: 'Status',
      key: 'status',
      render: (record: any) => (
        <Tag color={record.status === 'completed' ? 'green' : record.status === 'in-progress' ? 'blue' : 'orange'}>
          {record.status}
        </Tag>
      )
    },
    {
      title: 'Notes',
      dataIndex: 'notes',
      key: 'notes',
      ellipsis: true
    }
  ]

  const totalPatients = new Set(appointments.map(a => a.patient?.name).filter(Boolean)).size
  const avgSeverity = appointments.length > 0 
    ? (appointments.reduce((sum, a) => sum + (a.pre_consult_summary?.severity_score || 0), 0) / appointments.length).toFixed(1)
    : '0.0'

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
        <Title level={2} className="mb-6">Appointment History</Title>

        {/* Summary Cards */}
        <Row gutter={16} className="mb-6">
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">{appointments.length}</Title>
              <Text className="text-gray-500">Total Appointments</Text>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">{avgSeverity}</Title>
              <Text className="text-gray-500">Average Severity</Text>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card className="text-center shadow-sm">
              <Title level={3} className="!mb-0">{totalPatients}</Title>
              <Text className="text-gray-500">Unique Patients</Text>
            </Card>
          </Col>
        </Row>

        {/* Filters */}
        <Card className="mb-6 shadow-sm">
          <Row gutter={16} align="middle">
            <Col xs={24} sm={8}>
              <Text strong className="block mb-2">Date Range</Text>
              <RangePicker className="w-full" />
            </Col>
            <Col xs={24} sm={6}>
              <Text strong className="block mb-2">Severity Level</Text>
              <Select 
                className="w-full" 
                placeholder="All Severities"
                value={severityFilter}
                onChange={setSeverityFilter}
                allowClear
              >
                <Select.Option value="low">Low (1-4)</Select.Option>
                <Select.Option value="moderate">Moderate (5-6)</Select.Option>
                <Select.Option value="high">High (7-8)</Select.Option>
                <Select.Option value="emergency">Emergency (9-10)</Select.Option>
              </Select>
            </Col>
            <Col xs={24} sm={6}>
              <Text strong className="block mb-2">Consultation Type</Text>
              <Select 
                className="w-full" 
                placeholder="All Types"
                value={typeFilter}
                onChange={setTypeFilter}
                allowClear
              >
                <Select.Option value="online">Online</Select.Option>
                <Select.Option value="in-person">In-Person</Select.Option>
              </Select>
            </Col>
            <Col xs={24} sm={4}>
              <Button 
                type="primary" 
                icon={<FilterOutlined />} 
                onClick={handleFilter}
                className="w-full mt-6"
              >
                Apply Filters
              </Button>
            </Col>
          </Row>
        </Card>

        {/* Appointments Table */}
        <Card className="shadow-sm">
          <Table 
            columns={columns} 
            dataSource={filteredData}
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        </Card>
      </div>
    </div>
  )
}
