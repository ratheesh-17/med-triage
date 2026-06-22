import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card,
  Row,
  Col,
  Typography,
  Button,
  DatePicker,
  Select,
  Input,
  Tag,
  Space,
  Divider,
  Result,
  Spin
} from 'antd'
import {
  CheckCircleFilled,
  CalendarOutlined,
  ClockCircleOutlined,
  EnvironmentOutlined,
  UserOutlined,
  CheckCircleOutlined
} from '@ant-design/icons'
import dayjs, { Dayjs } from 'dayjs'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input
const { Option } = Select

export default function AppointmentBooking() {
  const { doctorId } = useParams()
  const navigate = useNavigate()
  
  const [doctor, setDoctor] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [booking, setBooking] = useState(false)
  const [paymentStep, setPaymentStep] = useState(false)
  const [success, setSuccess] = useState(false)
  
  // Booking form state
  const [selectedDate, setSelectedDate] = useState<Dayjs | null>(null)
  const [selectedTime, setSelectedTime] = useState<string>('')
  const [consultationType, setConsultationType] = useState<'online' | 'in-person'>('in-person')
  const [symptomNotes, setSymptomNotes] = useState('')
  const [familyMember, setFamilyMember] = useState<number | null>(null)
  const [familyMembers, setFamilyMembers] = useState<any[]>([])
  const [availableSlots, setAvailableSlots] = useState<string[]>([])
  const [loadingSlots, setLoadingSlots] = useState(false)

  useEffect(() => {
    loadDoctorDetails()
    loadFamilyMembers()
  }, [doctorId])

  const loadDoctorDetails = async () => {
    setLoading(true)
    try {
      const response = await api.get(`/doctors/${doctorId}`)
      setDoctor(response.data)
    } catch (error) {
      toast.error('Failed to load doctor details')
    } finally {
      setLoading(false)
    }
  }

  const loadFamilyMembers = async () => {
    try {
      const response = await api.get('/family')
      setFamilyMembers(response.data.family_members || [])
    } catch (error) {
      console.error('Failed to load family members')
    }
  }

  const loadAvailableSlots = async (date: string) => {
    if (!doctorId) return
    setLoadingSlots(true)
    try {
      const response = await api.get(`/doctor/slots/${doctorId}?date=${date}`)
      if (response.data.slots && response.data.slots.length > 0) {
        setAvailableSlots(response.data.slots)
      } else {
        // Default slots if none exist
        setAvailableSlots([
          '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
          '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM',
          '05:00 PM', '05:30 PM'
        ])
      }
    } catch (error) {
      // Use default slots on error
      setAvailableSlots([
        '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
        '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM',
        '05:00 PM', '05:30 PM'
      ])
    } finally {
      setLoadingSlots(false)
    }
  }

  useEffect(() => {
    if (selectedDate) {
      loadAvailableSlots(selectedDate.format('YYYY-MM-DD'))
    }
  }, [selectedDate])

  const handleBooking = async () => {
    if (!selectedDate || !selectedTime) {
      toast.error('Please select date and time')
      return
    }

    // Show payment confirmation step
    setPaymentStep(true)
  }

  const handlePaymentConfirm = async () => {
    setBooking(true)
    try {
      // Simulate payment processing
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Book appointment
      await api.post('/appointments', {
        doctor_id: Number(doctorId),
        date: selectedDate?.format('YYYY-MM-DD'),
        time: selectedTime,
        slot_type: consultationType,
        symptom_notes: symptomNotes,
        family_member_id: familyMember
      })
      
      setPaymentStep(false)
      setSuccess(true)
      toast.success('Payment confirmed & Appointment booked!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to book appointment')
    } finally {
      setBooking(false)
    }
  }

  const disabledDate = (current: Dayjs) => {
    // Disable past dates and dates more than 30 days in future
    return current && (current < dayjs().startOf('day') || current > dayjs().add(30, 'day'))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Spin size="large" />
      </div>
    )
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <Card style={{ maxWidth: 600, width: '100%', borderRadius: 16, boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
          <Result
            status="success"
            icon={<CheckCircleFilled style={{ fontSize: 72, color: '#52c41a' }} />}
            title={<Title level={2} className="!mb-2">Payment Confirmed!</Title>}
            subTitle={
              <div className="space-y-4">
                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <Text strong className="text-green-700 block mb-2">✓ Payment Successful</Text>
                  <Text className="text-green-600">Amount Paid: ₹{doctor?.fees}</Text>
                </div>
                <Paragraph className="text-lg">Your appointment has been confirmed with {doctor?.name}</Paragraph>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <Text><CalendarOutlined className="mr-2" /> <strong>Date:</strong> {selectedDate?.format('DD MMM YYYY')}</Text>
                    <Text><ClockCircleOutlined className="mr-2" /> <strong>Time:</strong> {selectedTime}</Text>
                    <Text><EnvironmentOutlined className="mr-2" /> <strong>Type:</strong> {consultationType === 'online' ? 'Online Consultation' : 'In-Person Visit'}</Text>
                    <Text><UserOutlined className="mr-2" /> <strong>Doctor:</strong> {doctor?.name}</Text>
                  </Space>
                </div>
              </div>
            }
            extra={[
              <Button type="primary" size="large" key="appointments" onClick={() => navigate('/patient/appointments')}>
                View My Appointments
              </Button>,
              <Button size="large" key="dashboard" onClick={() => navigate('/patient/dashboard')}>
                Return to Dashboard
              </Button>
            ]}
          />
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <Title level={2} className="!mb-6">Book Appointment</Title>

        <Row gutter={[24, 24]}>
          {/* Left Column - Booking Form */}
          <Col xs={24} lg={16}>
            {/* Doctor Summary Card */}
            <Card className="mb-6" style={{ borderRadius: 12 }}>
              <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                  <UserOutlined style={{ fontSize: 32, color: '#1890FF' }} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <Title level={4} className="!mb-0">{doctor?.name}</Title>
                    <CheckCircleFilled style={{ color: '#1890FF', fontSize: 18 }} />
                  </div>
                  <Text className="text-gray-600 block">{doctor?.specialization}</Text>
                  <Text className="text-gray-500 text-sm">{doctor?.hospital}</Text>
                </div>
              </div>
            </Card>

            {/* Date Selection */}
            <Card title="Select Date" className="mb-6" style={{ borderRadius: 12 }}>
              <DatePicker
                value={selectedDate}
                onChange={setSelectedDate}
                disabledDate={disabledDate}
                size="large"
                style={{ width: '100%' }}
                format="DD MMM YYYY"
              />
            </Card>

            {/* Time Slot Selection */}
            {selectedDate && (
              <Card title="Select Time Slot" className="mb-6" style={{ borderRadius: 12 }}>
                {loadingSlots ? (
                  <div className="text-center py-8">
                    <Spin />
                  </div>
                ) : availableSlots.length > 0 ? (
                  <div className="grid grid-cols-4 gap-2">
                    {availableSlots.map((slot) => (
                      <Button
                        key={slot}
                        type={selectedTime === slot ? 'primary' : 'default'}
                        onClick={() => setSelectedTime(slot)}
                        className="!h-12"
                      >
                        {slot}
                      </Button>
                    ))}
                  </div>
                ) : (
                  <Text className="text-gray-500">No slots available for this date</Text>
                )}
              </Card>
            )}

            {/* Consultation Type */}
            <Card title="Consultation Type" className="mb-6" style={{ borderRadius: 12 }}>
              <Row gutter={16}>
                <Col span={12}>
                  <Card
                    hoverable
                    className={consultationType === 'online' ? 'border-2 border-blue-500' : ''}
                    onClick={() => setConsultationType('online')}
                  >
                    <div className="text-center">
                      <CheckCircleOutlined
                        style={{
                          fontSize: 32,
                          color: consultationType === 'online' ? '#1890FF' : '#d9d9d9',
                          marginBottom: 8
                        }}
                      />
                      <Title level={5} className="!mb-1">Online</Title>
                      <Text className="text-gray-500 text-sm">Video Consultation</Text>
                    </div>
                  </Card>
                </Col>
                <Col span={12}>
                  <Card
                    hoverable
                    className={consultationType === 'in-person' ? 'border-2 border-blue-500' : ''}
                    onClick={() => setConsultationType('in-person')}
                  >
                    <div className="text-center">
                      <EnvironmentOutlined
                        style={{
                          fontSize: 32,
                          color: consultationType === 'in-person' ? '#1890FF' : '#d9d9d9',
                          marginBottom: 8
                        }}
                      />
                      <Title level={5} className="!mb-1">In-Person</Title>
                      <Text className="text-gray-500 text-sm">Visit Hospital</Text>
                    </div>
                  </Card>
                </Col>
              </Row>
            </Card>

            {/* Booking For */}
            <Card title="Booking For" className="mb-6" style={{ borderRadius: 12 }}>
              <Select
                value={familyMember}
                onChange={setFamilyMember}
                placeholder="Select who this appointment is for"
                size="large"
                style={{ width: '100%' }}
              >
                <Option value={null}>Myself</Option>
                {familyMembers.map((member) => (
                  <Option key={member.id} value={member.id}>
                    {member.name} ({member.relationship})
                  </Option>
                ))}
              </Select>
            </Card>

            {/* Symptom Notes */}
            <Card title="Additional Notes" className="mb-6" style={{ borderRadius: 12 }}>
              <TextArea
                rows={4}
                placeholder="Add any additional notes for the doctor about your symptoms or concerns..."
                value={symptomNotes}
                onChange={(e) => setSymptomNotes(e.target.value)}
                maxLength={500}
                showCount
              />
            </Card>
          </Col>

          {/* Right Column - Booking Summary */}
          <Col xs={24} lg={8}>
            <Card
              title="Booking Summary"
              style={{ borderRadius: 12, position: 'sticky', top: 24 }}
            >
              <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <div>
                  <Text className="text-gray-500 block mb-1">Doctor</Text>
                  <Text strong>{doctor?.name}</Text>
                </div>

                {selectedDate && (
                  <div>
                    <Text className="text-gray-500 block mb-1">Date</Text>
                    <Text strong>{selectedDate.format('DD MMM YYYY')}</Text>
                  </div>
                )}

                {selectedTime && (
                  <div>
                    <Text className="text-gray-500 block mb-1">Time</Text>
                    <Text strong>{selectedTime}</Text>
                  </div>
                )}

                <div>
                  <Text className="text-gray-500 block mb-1">Consultation Type</Text>
                  <Tag color="blue">{consultationType === 'online' ? 'Online' : 'In-Person'}</Tag>
                </div>

                <Divider className="!my-2" />

                <div className="flex justify-between items-center">
                  <Text strong className="text-lg">Consultation Fee</Text>
                  <Text strong className="text-xl text-blue-600">₹{doctor?.fees}</Text>
                </div>

                <Button
                  type="primary"
                  size="large"
                  block
                  onClick={handleBooking}
                  loading={booking}
                  disabled={!selectedDate || !selectedTime}
                  className="!h-14 !text-lg"
                >
                  Proceed to Payment
                </Button>

                <Text className="text-xs text-gray-500 text-center block">
                  By confirming, you agree to our terms and conditions
                </Text>
              </Space>
            </Card>
          </Col>
        </Row>

        {/* Payment Confirmation Modal */}
        <Card
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: paymentStep ? 'translate(-50%, -50%)' : 'translate(-50%, -50%) scale(0)',
            width: '90%',
            maxWidth: 500,
            zIndex: 1000,
            borderRadius: 16,
            boxShadow: '0 8px 40px rgba(0,0,0,0.2)',
            transition: 'transform 0.3s ease',
            opacity: paymentStep ? 1 : 0,
            pointerEvents: paymentStep ? 'auto' : 'none'
          }}
        >
          <div className="text-center">
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircleOutlined style={{ fontSize: 48, color: '#1890FF' }} />
            </div>
            <Title level={3} className="!mb-4">Confirm Payment</Title>
            
            <div className="bg-gray-50 p-4 rounded-lg mb-6 text-left">
              <Space direction="vertical" size="small" style={{ width: '100%' }}>
                <div className="flex justify-between">
                  <Text>Doctor:</Text>
                  <Text strong>{doctor?.name}</Text>
                </div>
                <div className="flex justify-between">
                  <Text>Date:</Text>
                  <Text strong>{selectedDate?.format('DD MMM YYYY')}</Text>
                </div>
                <div className="flex justify-between">
                  <Text>Time:</Text>
                  <Text strong>{selectedTime}</Text>
                </div>
                <div className="flex justify-between">
                  <Text>Type:</Text>
                  <Tag color="blue">{consultationType === 'online' ? 'Online' : 'In-Person'}</Tag>
                </div>
                <Divider className="!my-2" />
                <div className="flex justify-between items-center">
                  <Text strong className="text-lg">Total Amount:</Text>
                  <Text strong className="text-2xl text-blue-600">₹{doctor?.fees}</Text>
                </div>
              </Space>
            </div>

            <div className="bg-green-50 p-3 rounded-lg mb-6">
              <Text className="text-green-700">
                🔒 This is a demo payment. No actual charges will be made.
              </Text>
            </div>

            <Space size="middle" style={{ width: '100%' }}>
              <Button
                size="large"
                block
                onClick={() => setPaymentStep(false)}
                disabled={booking}
              >
                Cancel
              </Button>
              <Button
                type="primary"
                size="large"
                block
                onClick={handlePaymentConfirm}
                loading={booking}
                className="!h-12"
              >
                {booking ? 'Processing...' : 'Confirm & Pay'}
              </Button>
            </Space>
          </div>
        </Card>

        {/* Overlay */}
        {paymentStep && (
          <div
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              zIndex: 999
            }}
            onClick={() => !booking && setPaymentStep(false)}
          />
        )}
      </div>
    </div>
  )
}
