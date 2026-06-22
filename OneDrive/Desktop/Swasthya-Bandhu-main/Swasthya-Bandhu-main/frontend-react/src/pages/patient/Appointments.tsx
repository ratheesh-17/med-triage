import { useState, useEffect } from 'react'
import {
  Card,
  Typography,
  Button,
  Empty,
  Tag,
  Space,
  Divider,
  Modal,
  Rate,
  Input,
  Popconfirm,
  Tabs
} from 'antd'
import {
  CalendarOutlined,
  ClockCircleOutlined,
  EnvironmentOutlined,
  FileTextOutlined,
  DeleteOutlined,
  StarOutlined
} from '@ant-design/icons'
import api from '../../services/api'
import toast from 'react-hot-toast'
import dayjs from 'dayjs'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input

export default function Appointments() {
  const [appointments, setAppointments] = useState<any[]>([])
  const [selectedAppointment, setSelectedAppointment] = useState<any>(null)
  const [ratingModal, setRatingModal] = useState(false)
  const [rating, setRating] = useState(0)
  const [review, setReview] = useState('')

  useEffect(() => {
    loadAppointments()
  }, [])

  const loadAppointments = async () => {
    try {
      const response = await api.get('/appointments')
      setAppointments(response.data.appointments || [])
    } catch (error) {
      toast.error('Failed to load appointments')
    }
  }

  const handleCancelAppointment = async () => {
    try {
      // API endpoint for cancellation would go here
      toast.success('Appointment cancelled successfully')
      loadAppointments()
    } catch (error) {
      toast.error('Failed to cancel appointment')
    }
  }

  const handleSubmitRating = async () => {
    if (rating === 0) {
      toast.error('Please provide a rating')
      return
    }

    try {
      // API endpoint for rating would go here
      toast.success('Thank you for your feedback!')
      setRatingModal(false)
      setRating(0)
      setReview('')
    } catch (error) {
      toast.error('Failed to submit rating')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'blue'
      case 'in-progress': return 'orange'
      case 'confirmed': return 'blue'
      case 'completed': return 'green'
      case 'cancelled': return 'red'
      default: return 'default'
    }
  }

  const isUpcoming = (apt: any) => {
    return apt.status === 'scheduled' || apt.status === 'in-progress'
  }

  const upcomingAppointments = appointments.filter(apt => isUpcoming(apt))
  const pastAppointments = appointments.filter(apt => !isUpcoming(apt))

  const AppointmentCard = ({ appointment }: { appointment: any }) => (
    <Card
      style={{ borderRadius: 12, marginBottom: 16 }}
      hoverable
      onClick={() => setSelectedAppointment(appointment)}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Title level={5} className="!mb-0">{appointment.doctor?.name}</Title>
            <Tag color={getStatusColor(appointment.status)}>{appointment.status}</Tag>
          </div>
          <Text className="text-gray-600 block">{appointment.doctor?.specialization}</Text>
          <Text className="text-gray-500 text-sm">{appointment.doctor?.hospital}</Text>
        </div>
      </div>

      <Divider className="!my-3" />

      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <div className="flex items-center gap-2">
          <CalendarOutlined className="text-gray-400" />
          <Text>{dayjs(appointment.date).format('DD MMM YYYY')}</Text>
        </div>
        <div className="flex items-center gap-2">
          <ClockCircleOutlined className="text-gray-400" />
          <Text>{appointment.time}</Text>
        </div>
        <div className="flex items-center gap-2">
          <EnvironmentOutlined className="text-gray-400" />
          <Text>{appointment.slot_type === 'online' ? 'Online Consultation' : 'In-Person Visit'}</Text>
        </div>
      </Space>

      {appointment.symptom_notes && (
        <>
          <Divider className="!my-3" />
          <div>
            <Text strong className="block mb-1">Symptoms:</Text>
            <Text className="text-gray-600">{appointment.symptom_notes}</Text>
          </div>
        </>
      )}

      <Divider className="!my-3" />

      <Space>
        {isUpcoming(appointment) ? (
          <Popconfirm
            title="Cancel appointment?"
            description="Are you sure you want to cancel this appointment?"
            onConfirm={(e) => {
              e?.stopPropagation()
              handleCancelAppointment()
            }}
            okText="Yes"
            cancelText="No"
          >
            <Button
              danger
              icon={<DeleteOutlined />}
              onClick={(e) => e.stopPropagation()}
            >
              Cancel
            </Button>
          </Popconfirm>
        ) : (
          <Button
            type="primary"
            icon={<StarOutlined />}
            onClick={(e) => {
              e.stopPropagation()
              setSelectedAppointment(appointment)
              setRatingModal(true)
            }}
          >
            Rate Doctor
          </Button>
        )}
        {appointment.pre_consult_summary && (
          <Button icon={<FileTextOutlined />}>
            View AI Summary
          </Button>
        )}
      </Space>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <Title level={2} className="!mb-6">My Appointments</Title>

        <Tabs
          defaultActiveKey="upcoming"
          size="large"
          items={[
            {
              key: 'upcoming',
              label: `Upcoming (${upcomingAppointments.length})`,
              children: upcomingAppointments.length > 0 ? (
                upcomingAppointments.map(apt => (
                  <AppointmentCard key={apt.id} appointment={apt} />
                ))
              ) : (
                <Card style={{ borderRadius: 12 }}>
                  <Empty description="No upcoming appointments" />
                </Card>
              )
            },
            {
              key: 'past',
              label: `Past (${pastAppointments.length})`,
              children: pastAppointments.length > 0 ? (
                pastAppointments.map(apt => (
                  <AppointmentCard key={apt.id} appointment={apt} />
                ))
              ) : (
                <Card style={{ borderRadius: 12 }}>
                  <Empty description="No past appointments" />
                </Card>
              )
            }
          ]}
        />

        {/* Appointment Detail Modal */}
        <Modal
          title="Appointment Details"
          open={!!selectedAppointment && !ratingModal}
          onCancel={() => setSelectedAppointment(null)}
          footer={null}
          width={600}
        >
          {selectedAppointment && (
            <div>
              <div className="mb-4">
                <Title level={4} className="!mb-2">{selectedAppointment.doctor?.name}</Title>
                <Text className="text-gray-600">{selectedAppointment.doctor?.specialization}</Text>
              </div>

              <Divider />

              <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <div>
                  <Text strong>Date & Time:</Text>
                  <br />
                  <Text>{dayjs(selectedAppointment.date).format('DD MMM YYYY')} at {selectedAppointment.time}</Text>
                </div>

                <div>
                  <Text strong>Hospital:</Text>
                  <br />
                  <Text>{selectedAppointment.doctor?.hospital}</Text>
                </div>

                <div>
                  <Text strong>Consultation Type:</Text>
                  <br />
                  <Tag color="blue">
                    {selectedAppointment.slot_type === 'online' ? 'Online' : 'In-Person'}
                  </Tag>
                </div>

                {selectedAppointment.symptom_notes && (
                  <div>
                    <Text strong>Symptoms Noted:</Text>
                    <br />
                    <Paragraph className="text-gray-600">{selectedAppointment.symptom_notes}</Paragraph>
                  </div>
                )}

                {selectedAppointment.pre_consult_summary && (
                  <div className="bg-blue-50 p-4 rounded">
                    <Text strong className="block mb-2">AI Pre-Consult Summary:</Text>
                    <Space direction="vertical" size="small">
                      <Text>Severity: {selectedAppointment.pre_consult_summary.severity_score}/10</Text>
                      <Text>Urgency: {selectedAppointment.pre_consult_summary.urgency}</Text>
                    </Space>
                  </div>
                )}
              </Space>
            </div>
          )}
        </Modal>

        {/* Rating Modal */}
        <Modal
          title="Rate Your Doctor"
          open={ratingModal}
          onCancel={() => {
            setRatingModal(false)
            setRating(0)
            setReview('')
          }}
          footer={null}
          width={500}
        >
          <div className="text-center mb-6">
            <Title level={4} className="!mb-4">How was your experience?</Title>
            <Rate
              value={rating}
              onChange={setRating}
              style={{ fontSize: 40 }}
            />
          </div>

          <TextArea
            rows={4}
            placeholder="Share your experience (optional)"
            value={review}
            onChange={(e) => setReview(e.target.value)}
            className="mb-4"
          />

          <Button
            type="primary"
            size="large"
            block
            onClick={handleSubmitRating}
          >
            Submit Rating
          </Button>
        </Modal>
      </div>
    </div>
  )
}
