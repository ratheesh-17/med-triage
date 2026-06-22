import { useState, useEffect } from 'react'
import { Card, Button, Modal, Input, Tag, Descriptions, Typography, Row, Col, message, Spin } from 'antd'
import { CheckCircleOutlined, CloseCircleOutlined, InfoCircleOutlined, UserOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title, Text } = Typography
const { TextArea } = Input

export default function DoctorVerification() {
  const [activeTab] = useState('pending')
  const [rejectModal, setRejectModal] = useState(false)
  const [selectedDoctor, setSelectedDoctor] = useState<any>(null)
  const [rejectionReason, setRejectionReason] = useState('')
  const [pendingDoctors, setPendingDoctors] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (activeTab === 'pending') {
      fetchPendingDoctors()
    }
  }, [activeTab])

  const fetchPendingDoctors = async () => {
    try {
      setLoading(true)
      const response = await api.get('/admin/doctors/pending')
      console.log('Pending doctors response:', response.data)
      setPendingDoctors(response.data.doctors || [])
    } catch (err: any) {
      console.error('Error fetching doctors:', err)
      message.error(err.response?.data?.detail || 'Failed to fetch pending doctors')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = (doctor: any) => {
    Modal.confirm({
      title: 'Approve Doctor',
      content: 'Approving this doctor will make them immediately visible to patients. Confirm?',
      onOk: async () => {
        try {
          await api.post('/admin/doctors/approve', {
            doctor_id: doctor.id,
            approved: true
          })
          message.success(`Dr. ${doctor.name} approved successfully`)
          fetchPendingDoctors()
        } catch (err: any) {
          message.error(err.response?.data?.detail || 'Failed to approve doctor')
        }
      }
    })
  }

  const handleReject = (doctor: any) => {
    setSelectedDoctor(doctor)
    setRejectModal(true)
  }

  const submitRejection = async () => {
    if (!rejectionReason.trim()) {
      message.error('Please provide a rejection reason')
      return
    }
    try {
      await api.post('/admin/doctors/approve', {
        doctor_id: selectedDoctor.id,
        approved: false,
        rejection_reason: rejectionReason
      })
      message.success(`Dr. ${selectedDoctor.name} rejected`)
      setRejectModal(false)
      setRejectionReason('')
      fetchPendingDoctors()
    } catch (err: any) {
      message.error(err.response?.data?.detail || 'Failed to reject doctor')
    }
  }

  const handleRequestInfo = (doctor: any) => {
    message.info(`Information request sent to Dr. ${doctor.name}`)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2} className="mb-6">Doctor Verification Queue</Title>

        <Card>
          {loading ? (
            <div className="text-center py-12">
              <Spin size="large" />
            </div>
          ) : pendingDoctors.length === 0 ? (
            <div className="text-center py-12">
              <Text className="text-gray-500">No pending doctor applications</Text>
            </div>
          ) : (
            <div className="space-y-6">
                {pendingDoctors.map(doctor => (
                <Card key={doctor.id} className="shadow-sm">
                  <Row gutter={16}>
                    <Col span={4} className="text-center">
                      <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                        <UserOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                      </div>
                      <Tag color="orange">PENDING</Tag>
                    </Col>
                    <Col span={20}>
                      <Title level={4} className="!mb-4">{doctor.name}</Title>
                      
                      <Descriptions bordered column={2} size="small" className="mb-4">
                        <Descriptions.Item label="Phone">{doctor.phone}</Descriptions.Item>
                        <Descriptions.Item label="Specialization">{doctor.specialization}</Descriptions.Item>
                        <Descriptions.Item label="Experience">{doctor.experience}</Descriptions.Item>
                        <Descriptions.Item label="Hospital">{doctor.hospital}</Descriptions.Item>
                        <Descriptions.Item label="Medical Council Number" span={2}>
                          <Text strong className="text-blue-600">{doctor.medical_council_number}</Text>
                        </Descriptions.Item>
                      </Descriptions>

                      <div className="flex gap-2">
                        <Button
                          type="primary"
                          icon={<CheckCircleOutlined />}
                          onClick={() => handleApprove(doctor)}
                        >
                          Approve
                        </Button>
                        <Button
                          danger
                          icon={<CloseCircleOutlined />}
                          onClick={() => handleReject(doctor)}
                        >
                          Reject
                        </Button>
                        <Button
                          icon={<InfoCircleOutlined />}
                          onClick={() => handleRequestInfo(doctor)}
                        >
                          Request More Info
                        </Button>
                      </div>
                    </Col>
                  </Row>
                </Card>
                ))}
              </div>
            )}
        </Card>

        {/* Rejection Modal */}
        <Modal
          title="Reject Doctor Application"
          open={rejectModal}
          onCancel={() => setRejectModal(false)}
          onOk={submitRejection}
          okText="Confirm Rejection"
          okButtonProps={{ danger: true }}
        >
          <Text strong className="block mb-2">Doctor: {selectedDoctor?.name}</Text>
          <Text className="block mb-4">Please provide a reason for rejection (will be shown to doctor):</Text>
          <TextArea
            rows={4}
            value={rejectionReason}
            onChange={(e) => setRejectionReason(e.target.value)}
            placeholder="e.g., Medical Council Number could not be verified, Invalid credentials, etc."
          />
        </Modal>
      </div>
    </div>
  )
}
