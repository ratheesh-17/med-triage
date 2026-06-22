import { useState, useEffect } from 'react'
import { Card, Button, Descriptions, Tag, Typography, Row, Col, Spin, Alert } from 'antd'
import { CheckCircleOutlined, CloseCircleOutlined, ReloadOutlined, BugOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title, Text } = Typography

export default function AdminDebug() {
  const [loading, setLoading] = useState(false)
  const [systemStatus, setSystemStatus] = useState<any>(null)
  const [workflowTest, setWorkflowTest] = useState<any>(null)

  useEffect(() => {
    fetchSystemStatus()
    testWorkflow()
  }, [])

  const fetchSystemStatus = async () => {
    try {
      setLoading(true)
      const response = await api.get('/admin/debug/system-status')
      setSystemStatus(response.data)
    } catch (err) {
      console.error('Error fetching system status:', err)
    } finally {
      setLoading(false)
    }
  }

  const testWorkflow = async () => {
    try {
      const response = await api.get('/admin/debug/workflow-test')
      setWorkflowTest(response.data)
    } catch (err) {
      console.error('Error testing workflow:', err)
    }
  }

  const refreshAll = () => {
    fetchSystemStatus()
    testWorkflow()
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Title level={2}>
            <BugOutlined className="mr-2" />
            System Debug Dashboard
          </Title>
          <Button icon={<ReloadOutlined />} onClick={refreshAll} loading={loading}>
            Refresh All
          </Button>
        </div>

        {/* Workflow Test Results */}
        {workflowTest && (
          <Alert
            message={workflowTest.overall_status === 'PASS' ? 'All Systems Operational' : 'System Issues Detected'}
            description={workflowTest.message}
            type={workflowTest.overall_status === 'PASS' ? 'success' : 'error'}
            showIcon
            className="mb-6"
          />
        )}

        {loading ? (
          <div className="text-center py-12">
            <Spin size="large" />
          </div>
        ) : (
          <>
            {/* System Counts */}
            <Card title="System Statistics" className="mb-6">
              <Row gutter={16}>
                <Col span={6}>
                  <Card className="text-center bg-blue-50">
                    <Title level={2} className="!mb-0">{systemStatus?.counts?.total_patients || 0}</Title>
                    <Text>Total Patients</Text>
                  </Card>
                </Col>
                <Col span={6}>
                  <Card className="text-center bg-green-50">
                    <Title level={2} className="!mb-0">{systemStatus?.counts?.approved_doctors || 0}</Title>
                    <Text>Approved Doctors</Text>
                  </Card>
                </Col>
                <Col span={6}>
                  <Card className="text-center bg-yellow-50">
                    <Title level={2} className="!mb-0">{systemStatus?.counts?.pending_doctors || 0}</Title>
                    <Text>Pending Doctors</Text>
                  </Card>
                </Col>
                <Col span={6}>
                  <Card className="text-center bg-purple-50">
                    <Title level={2} className="!mb-0">{systemStatus?.counts?.total_appointments || 0}</Title>
                    <Text>Total Appointments</Text>
                  </Card>
                </Col>
              </Row>

              <Descriptions bordered className="mt-6" column={2}>
                <Descriptions.Item label="Total Doctors">{systemStatus?.counts?.total_doctors || 0}</Descriptions.Item>
                <Descriptions.Item label="Rejected Doctors">{systemStatus?.counts?.rejected_doctors || 0}</Descriptions.Item>
                <Descriptions.Item label="AI Sessions">{systemStatus?.counts?.total_ai_sessions || 0}</Descriptions.Item>
                <Descriptions.Item label="System Status">
                  <Tag color="green">Operational</Tag>
                </Descriptions.Item>
              </Descriptions>
            </Card>

            {/* Workflow Tests */}
            {workflowTest && (
              <Card title="Workflow Connectivity Tests" className="mb-6">
                <div className="space-y-2">
                  {Object.entries(workflowTest.tests).map(([key, value]: [string, any]) => {
                    if (typeof value === 'boolean') {
                      return (
                        <div key={key} className="flex items-center justify-between p-2 border-b">
                          <Text>{key.replace(/_/g, ' ').toUpperCase()}</Text>
                          {value ? (
                            <Tag icon={<CheckCircleOutlined />} color="success">PASS</Tag>
                          ) : (
                            <Tag icon={<CloseCircleOutlined />} color="error">FAIL</Tag>
                          )}
                        </div>
                      )
                    } else if (typeof value === 'number') {
                      return (
                        <div key={key} className="flex items-center justify-between p-2 border-b">
                          <Text>{key.replace(/_/g, ' ').toUpperCase()}</Text>
                          <Tag color="blue">{value}</Tag>
                        </div>
                      )
                    }
                    return null
                  })}
                </div>
              </Card>
            )}

            {/* Recent Doctors */}
            <Card title="Recent Doctor Registrations" className="mb-6">
              {systemStatus?.recent_doctors?.map((doctor: any) => (
                <div key={doctor.id} className="flex items-center justify-between p-3 border-b">
                  <div>
                    <Text strong>{doctor.name}</Text>
                    <br />
                    <Text className="text-gray-500 text-sm">{doctor.phone}</Text>
                  </div>
                  <div className="text-right">
                    <Tag color={
                      doctor.status === 'approved' ? 'green' :
                      doctor.status === 'pending' ? 'orange' : 'red'
                    }>
                      {doctor.status.toUpperCase()}
                    </Tag>
                    <br />
                    <Text className="text-xs text-gray-400">{new Date(doctor.registered_at).toLocaleString()}</Text>
                  </div>
                </div>
              ))}
            </Card>

            {/* Recent Patients */}
            <Card title="Recent Patient Registrations">
              {systemStatus?.recent_patients?.map((patient: any) => (
                <div key={patient.id} className="flex items-center justify-between p-3 border-b">
                  <div>
                    <Text strong>{patient.name}</Text>
                    <br />
                    <Text className="text-gray-500 text-sm">{patient.phone}</Text>
                  </div>
                  <Text className="text-xs text-gray-400">{new Date(patient.registered_at).toLocaleString()}</Text>
                </div>
              ))}
            </Card>
          </>
        )}
      </div>
    </div>
  )
}
