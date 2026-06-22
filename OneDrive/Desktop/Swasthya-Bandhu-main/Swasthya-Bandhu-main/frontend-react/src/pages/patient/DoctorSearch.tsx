import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  Card,
  Row,
  Col,
  Input,
  Select,
  Button,
  Typography,
  Badge,
  Tag,
  Spin,
  Empty,
  Space
} from 'antd'
import {
  EnvironmentOutlined,
  CheckCircleFilled,
  CalendarOutlined,
  DollarOutlined,
  StarFilled,
  UnorderedListOutlined,
  EnvironmentFilled
} from '@ant-design/icons'
import MapView from '../../components/MapView'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text, Paragraph } = Typography
const { Option } = Select

interface Doctor {
  id: number
  name: string
  specialization: string
  hospital: string
  rating: number
  experience: string
  fees: number
  distance_km: number
  location: { lat: number; lng: number }
}

export default function DoctorSearch() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [loading, setLoading] = useState(false)
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list')
  
  // Filters
  const [specialization, setSpecialization] = useState(searchParams.get('specialization') || 'General Physician')
  const [location, setLocation] = useState('Coimbatore')
  const [sortBy, setSortBy] = useState<'distance' | 'rating'>('distance')
  const userLocation = { lat: 11.0081, lng: 76.9650 }

  useEffect(() => {
    searchDoctors()
  }, [specialization, sortBy])

  const searchDoctors = async () => {
    setLoading(true)
    try {
      const response = await api.get('/doctors/search', {
        params: {
          specialization,
          user_lat: userLocation.lat,
          user_lng: userLocation.lng
        }
      })
      
      let results = response.data.doctors || []
      
      // Sort results
      if (sortBy === 'rating') {
        results = results.sort((a: Doctor, b: Doctor) => b.rating - a.rating)
      }
      
      setDoctors(results)
      
      if (results.length === 0) {
        toast.error('No doctors found for this specialization')
      }
    } catch (error: any) {
      console.error('Search error:', error)
      const detail = error.response?.data?.detail
      if (Array.isArray(detail)) {
        toast.error(`Error: ${detail[0]?.msg || 'Failed to search doctors'}`)
      } else if (typeof detail === 'string') {
        toast.error(detail)
      } else {
        toast.error('Failed to search doctors')
      }
      setDoctors([])
    } finally {
      setLoading(false)
    }
  }

  const specializations = [
    'General Physician',
    'Cardiologist',
    'Dermatologist',
    'Pediatrician',
    'Orthopedic Surgeon',
    'Neurologist',
    'Psychiatrist',
    'Gynecologist',
    'ENT Specialist',
    'Ophthalmologist',
    'Pulmonologist',
    'Gastroenterologist'
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Title level={2} className="!mb-2">Find Verified Doctors</Title>
          <Text className="text-gray-500">Book appointments with top-rated specialists near you</Text>
        </div>

        {/* Filter Bar */}
        <Card className="mb-6" style={{ borderRadius: 12 }}>
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} md={8}>
              <Text strong className="block mb-2">Specialization</Text>
              <Select
                value={specialization}
                onChange={setSpecialization}
                style={{ width: '100%' }}
                size="large"
                showSearch
              >
                {specializations.map(spec => (
                  <Option key={spec} value={spec}>{spec}</Option>
                ))}
              </Select>
            </Col>
            
            <Col xs={24} md={6}>
              <Text strong className="block mb-2">Location</Text>
              <Input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                prefix={<EnvironmentOutlined />}
                size="large"
                disabled
              />
            </Col>
            
            <Col xs={24} md={6}>
              <Text strong className="block mb-2">Sort By</Text>
              <Select
                value={sortBy}
                onChange={setSortBy}
                style={{ width: '100%' }}
                size="large"
              >
                <Option value="distance">Nearest First</Option>
                <Option value="rating">Top Rated First</Option>
              </Select>
            </Col>
            
            <Col xs={24} md={4}>
              <Text strong className="block mb-2">View</Text>
              <Space>
                <Button
                  type={viewMode === 'list' ? 'primary' : 'default'}
                  icon={<UnorderedListOutlined />}
                  onClick={() => setViewMode('list')}
                  size="large"
                >
                  List
                </Button>
                <Button
                  type={viewMode === 'map' ? 'primary' : 'default'}
                  icon={<EnvironmentFilled />}
                  onClick={() => setViewMode('map')}
                  size="large"
                >
                  Map
                </Button>
              </Space>
            </Col>
          </Row>
        </Card>

        {/* Results */}
        {loading ? (
          <div className="text-center py-20">
            <Spin size="large" />
            <Paragraph className="mt-4 text-gray-500">Searching for doctors...</Paragraph>
          </div>
        ) : doctors.length === 0 ? (
          <Card style={{ borderRadius: 12 }}>
            <Empty
              description="No doctors found for this specialization"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          </Card>
        ) : (
          <div>
            <div className="mb-4">
              <Text className="text-gray-600">
                Found <strong>{doctors.length}</strong> {specialization}s near you
              </Text>
            </div>
            
            <Row gutter={[16, 16]}>
              {doctors.map((doctor) => (
                <Col xs={24} lg={12} key={doctor.id}>
                  <Card
                    hoverable
                    style={{ borderRadius: 12, height: '100%' }}
                    className="doctor-card"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Title level={4} className="!mb-0">{doctor.name}</Title>
                          <CheckCircleFilled style={{ color: '#1890FF', fontSize: 20 }} />
                        </div>
                        <Text className="text-gray-600">{doctor.specialization}</Text>
                      </div>
                      <Badge
                        count={
                          <div className="flex items-center gap-1 bg-green-100 px-3 py-1 rounded-full">
                            <StarFilled style={{ color: '#faad14', fontSize: 14 }} />
                            <Text strong>{doctor.rating}</Text>
                          </div>
                        }
                      />
                    </div>

                    <div className="space-y-2 mb-4">
                      <div className="flex items-center gap-2">
                        <EnvironmentOutlined className="text-gray-400" />
                        <Text className="text-gray-600">{doctor.hospital}</Text>
                      </div>
                      
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <CalendarOutlined className="text-gray-400" />
                          <Text className="text-gray-600">{doctor.experience}</Text>
                        </div>
                        <div className="flex items-center gap-2">
                          <DollarOutlined className="text-gray-400" />
                          <Text className="text-gray-600">₹{doctor.fees}</Text>
                        </div>
                      </div>
                      
                      <div>
                        <Tag color="blue" icon={<EnvironmentOutlined />}>
                          {doctor.distance_km.toFixed(1)} km away
                        </Tag>
                      </div>
                    </div>

                    {/* Available Slots */}
                    <div className="mb-4">
                      <Text strong className="block mb-2">Available Today:</Text>
                      <Space wrap>
                        <Tag color="green">10:00 AM</Tag>
                        <Tag color="green">2:00 PM</Tag>
                        <Tag color="green">4:30 PM</Tag>
                      </Space>
                    </div>

                    <Row gutter={8}>
                      <Col span={12}>
                        <Button
                          type="primary"
                          block
                          size="large"
                          onClick={() => navigate(`/patient/book-appointment/${doctor.id}`)}
                        >
                          Book Appointment
                        </Button>
                      </Col>
                      <Col span={12}>
                        <Button
                          block
                          size="large"
                          icon={<EnvironmentOutlined />}
                          onClick={() => {
                            setViewMode('map')
                            // Scroll to map or focus on this doctor
                          }}
                        >
                          View on Map
                        </Button>
                      </Col>
                    </Row>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        )}

        {/* Map View */}
        {viewMode === 'map' && doctors.length > 0 && (
          <Card className="mt-6" style={{ borderRadius: 12 }}>
            <MapView doctors={doctors} userLocation={userLocation} />
          </Card>
        )}
      </div>
    </div>
  )
}
