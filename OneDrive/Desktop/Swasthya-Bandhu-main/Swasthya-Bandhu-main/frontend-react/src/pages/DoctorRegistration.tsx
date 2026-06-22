import { useState } from 'react'
import { Form, Input, Button, Steps, Select, Upload, InputNumber, Checkbox, Typography, Card, Row, Col, Tooltip } from 'antd'
import { UserOutlined, MedicineBoxOutlined, CalendarOutlined, UploadOutlined, InfoCircleOutlined, CheckCircleOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { authService } from '../services/auth'

const { Title, Paragraph, Text } = Typography
const { TextArea } = Input

const SPECIALIZATIONS = [
  'General Physician', 'Cardiologist', 'Dermatologist', 'Pediatrician', 'Orthopedic',
  'Gynecologist', 'Neurologist', 'Psychiatrist', 'ENT Specialist', 'Ophthalmologist',
  'Dentist', 'Gastroenterologist', 'Urologist', 'Pulmonologist', 'Endocrinologist'
]

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const TIME_SLOTS = ['Morning', 'Afternoon', 'Evening']

export default function DoctorRegistration() {
  const [current, setCurrent] = useState(0)
  const [form] = Form.useForm()
  const [profilePhoto, setProfilePhoto] = useState<string>('')
  const [availability, setAvailability] = useState<Record<string, string[]>>({})
  const [submitted, setSubmitted] = useState(false)
  const navigate = useNavigate()

  const handlePhotoUpload = (file: File) => {
    const reader = new FileReader()
    reader.onload = (e) => setProfilePhoto(e.target?.result as string)
    reader.readAsDataURL(file)
    return false
  }

  const toggleAvailability = (day: string, slot: string) => {
    setAvailability(prev => {
      const daySlots = prev[day] || []
      const updated = daySlots.includes(slot)
        ? daySlots.filter(s => s !== slot)
        : [...daySlots, slot]
      return { ...prev, [day]: updated }
    })
  }

  const handleNext = async () => {
    try {
      // Validate only current step fields
      const fieldsToValidate = [
        current === 0 ? ['fullName', 'phone', 'email', 'age'] : [],
        current === 1 ? ['specialization', 'medicalCouncilNumber', 'experience', 'hospitalAffiliation', 'hospitalAddress', 'latitude', 'longitude', 'consultationFee', 'consultationDuration', 'consultationTypes'] : [],
        current === 2 ? ['bio'] : []
      ][current]
      
      await form.validateFields(fieldsToValidate)
      setCurrent(current + 1)
    } catch (err) {
      toast.error('Please fill all required fields')
    }
  }

  const handleSubmit = async () => {
    try {
      // Validate all fields from all steps
      const values = await form.validateFields()
      
      console.log('Form values:', values)
      
      // Validate required fields exist
      if (!values.phone || !values.fullName || !values.specialization || !values.medicalCouncilNumber) {
        toast.error('Please fill all required fields in all steps')
        return
      }
      
      const payload = {
        phone: String(values.phone).trim(),
        name: String(values.fullName).trim(),
        specialization: String(values.specialization),
        hospital: String(values.hospitalAffiliation).trim(),
        experience: String(values.experience),
        fees: parseInt(String(values.consultationFee)),
        location_lat: parseFloat(String(values.latitude)),
        location_lng: parseFloat(String(values.longitude)),
        medical_council_number: String(values.medicalCouncilNumber).trim()
      }
      
      console.log('Payload being sent:', payload)
      
      await authService.registerDoctor(payload)
      toast.success('Registration submitted for verification')
      setSubmitted(true)
    } catch (err: any) {
      console.error('Registration error:', err)
      
      if (err.errorFields) {
        toast.error('Please fill all required fields correctly')
        return
      }
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail
        if (Array.isArray(detail)) {
          const firstError = detail[0]
          const field = firstError.loc[firstError.loc.length - 1]
          toast.error(`${field}: ${firstError.msg}`)
        } else {
          toast.error(String(detail))
        }
      } else {
        toast.error('Registration failed. Please try again.')
      }
    }
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-6">
        <Card className="max-w-2xl w-full text-center shadow-xl">
          <div className="py-8">
            <CheckCircleOutlined style={{ fontSize: 80, color: '#52c41a' }} />
            <Title level={2} className="!mt-6 !mb-4">Registration Submitted!</Title>
            <div className="inline-block px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full mb-6">
              <Text strong>⏳ Pending Verification</Text>
            </div>
            <Paragraph className="text-gray-600 text-lg mb-8">
              Your profile has been submitted for verification. You will receive an OTP on your registered number once the admin approves your account. This typically takes 24 hours.
            </Paragraph>
            <Button type="primary" size="large" onClick={() => navigate('/login')}>
              Go to Login
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <Title level={2}>Doctor Registration</Title>
          <Paragraph className="text-gray-600">Join Swasthya Bandhu as a verified healthcare professional</Paragraph>
        </div>

        <Card className="shadow-xl">
          <Steps current={current} className="mb-8">
            <Steps.Step title="Personal Details" icon={<UserOutlined />} />
            <Steps.Step title="Professional Details" icon={<MedicineBoxOutlined />} />
            <Steps.Step title="Bio & Availability" icon={<CalendarOutlined />} />
          </Steps>

          <Form form={form} layout="vertical" size="large">
            <div style={{ display: current === 0 ? 'block' : 'none' }}>
              <div>
                <Row gutter={16}>
                  <Col span={24} className="text-center mb-6">
                    <Upload
                      accept="image/*"
                      showUploadList={false}
                      beforeUpload={handlePhotoUpload}
                    >
                      <div className="cursor-pointer">
                        {profilePhoto ? (
                          <img src={profilePhoto} alt="Profile" className="w-32 h-32 rounded-full mx-auto object-cover border-4 border-blue-200" />
                        ) : (
                          <div className="w-32 h-32 rounded-full mx-auto bg-gray-200 flex items-center justify-center border-4 border-gray-300">
                            <UserOutlined style={{ fontSize: 48, color: '#999' }} />
                          </div>
                        )}
                        <Button icon={<UploadOutlined />} className="mt-4">Upload Photo</Button>
                      </div>
                    </Upload>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="fullName" label="Full Name" rules={[{ required: true }]}>
                      <Input placeholder="Dr. John Doe" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="phone" label="Phone Number" rules={[{ required: true, pattern: /^[0-9]{10}$/, message: 'Enter 10 digit number' }]}>
                      <Input placeholder="9876543210" maxLength={10} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="email" label="Email Address" rules={[{ required: true, type: 'email' }]}>
                      <Input placeholder="doctor@example.com" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="age" label="Age" rules={[{ required: true }]}>
                      <InputNumber min={25} max={80} className="w-full" placeholder="35" />
                    </Form.Item>
                  </Col>
                </Row>
              </div>
            </div>

            <div style={{ display: current === 1 ? 'block' : 'none' }}>
              <div>
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item name="specialization" label="Medical Specialization" rules={[{ required: true }]}>
                      <Select placeholder="Select specialization">
                        {SPECIALIZATIONS.map(s => <Select.Option key={s} value={s}>{s}</Select.Option>)}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item 
                      name="medicalCouncilNumber" 
                      label={
                        <span>
                          Medical Council Registration Number{' '}
                          <Tooltip title="Your state medical council registration number (e.g., MCI/12345/2020)">
                            <InfoCircleOutlined className="text-blue-500" />
                          </Tooltip>
                        </span>
                      }
                      rules={[{ required: true }]}
                    >
                      <Input placeholder="MCI/12345/2020" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="experience" label="Years of Experience" rules={[{ required: true }]}>
                      <InputNumber min={0} max={50} className="w-full" placeholder="10" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="hospitalAffiliation" label="Hospital/Clinic Affiliation" rules={[{ required: true }]}>
                      <Input placeholder="City Hospital" />
                    </Form.Item>
                  </Col>
                  <Col span={24}>
                    <Form.Item name="hospitalAddress" label="Hospital Address" rules={[{ required: true }]}>
                      <Input placeholder="123 Medical Street, Coimbatore" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="latitude" label="Location Latitude" rules={[{ required: true }]}>
                      <InputNumber className="w-full" placeholder="11.0168" step={0.0001} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="longitude" label="Location Longitude" rules={[{ required: true }]}>
                      <InputNumber className="w-full" placeholder="76.9558" step={0.0001} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="consultationFee" label="Consultation Fee (₹)" rules={[{ required: true }]}>
                      <InputNumber min={0} className="w-full" placeholder="500" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="consultationDuration" label="Avg. Consultation Duration (mins)" rules={[{ required: true }]}>
                      <InputNumber min={10} max={120} className="w-full" placeholder="30" />
                    </Form.Item>
                  </Col>
                  <Col span={24}>
                    <Form.Item name="consultationTypes" label="Consultation Types" rules={[{ required: true }]}>
                      <Checkbox.Group>
                        <Checkbox value="online">Online</Checkbox>
                        <Checkbox value="in-person">In-Person</Checkbox>
                      </Checkbox.Group>
                    </Form.Item>
                  </Col>
                </Row>
              </div>
            </div>

            <div style={{ display: current === 2 ? 'block' : 'none' }}>
              <div>
                <Form.Item name="bio" label="Professional Bio" rules={[{ required: true }]}>
                  <TextArea rows={4} placeholder="Brief professional summary (2-3 sentences)" maxLength={300} showCount />
                </Form.Item>

                <div className="mb-6">
                  <Text strong className="block mb-4">Weekly Availability Pattern</Text>
                  <div className="border rounded-lg overflow-hidden">
                    <table className="w-full">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="p-3 text-left border-r">Day</th>
                          {TIME_SLOTS.map(slot => (
                            <th key={slot} className="p-3 text-center border-r last:border-r-0">{slot}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {DAYS.map(day => (
                          <tr key={day} className="border-t">
                            <td className="p-3 font-medium border-r bg-gray-50">{day}</td>
                            {TIME_SLOTS.map(slot => (
                              <td key={slot} className="p-3 text-center border-r last:border-r-0">
                                <Checkbox
                                  checked={availability[day]?.includes(slot)}
                                  onChange={() => toggleAvailability(day, slot)}
                                />
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-between mt-8">
              {current > 0 && (
                <Button size="large" onClick={() => setCurrent(current - 1)}>
                  Previous
                </Button>
              )}
              {current < 2 ? (
                <Button type="primary" size="large" onClick={handleNext} className="ml-auto">
                  Next
                </Button>
              ) : (
                <Button type="primary" size="large" onClick={handleSubmit} className="ml-auto">
                  Submit for Verification
                </Button>
              )}
            </div>
          </Form>
        </Card>
      </div>
    </div>
  )
}
