import { useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import { Button, Typography, Space, Drawer } from 'antd'
import { CheckCircleFilled } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const { Title, Text } = Typography

// Fix Leaflet default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

interface Doctor {
  id: number
  name: string
  specialization: string
  hospital: string
  rating: number
  fees: number
  location: { lat: number; lng: number }
}

interface MapViewProps {
  doctors: Doctor[]
  userLocation: { lat: number; lng: number }
}

export default function MapView({ doctors, userLocation }: MapViewProps) {
  const navigate = useNavigate()
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null)
  const [drawerVisible, setDrawerVisible] = useState(false)

  const handleDoctorClick = (doctor: Doctor) => {
    setSelectedDoctor(doctor)
    setDrawerVisible(true)
  }

  const calculateDistance = (lat1: number, lng1: number, lat2: number, lng2: number) => {
    const R = 6371 // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLng = (lng2 - lng1) * Math.PI / 180
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    return (R * c).toFixed(1)
  }

  return (
    <div style={{ height: '600px', width: '100%', borderRadius: 12, overflow: 'hidden' }}>
      <MapContainer
        center={[userLocation.lat, userLocation.lng]}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* User Location Marker (Blue) */}
        <Marker position={[userLocation.lat, userLocation.lng]}>
          <Popup>
            <div className="text-center">
              <Text strong>You are here</Text>
            </div>
          </Popup>
        </Marker>

        {/* Doctor Location Markers (Green) */}
        {doctors.map((doctor) => (
          <Marker
            key={doctor.id}
            position={[doctor.location.lat, doctor.location.lng]}
            eventHandlers={{
              click: () => handleDoctorClick(doctor)
            }}
          >
            <Popup>
              <div>
                <Text strong className="block">{doctor.name}</Text>
                <Text className="text-sm">{doctor.hospital}</Text>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Route Line */}
        {selectedDoctor && (
          <Polyline
            positions={[
              [userLocation.lat, userLocation.lng],
              [selectedDoctor.location.lat, selectedDoctor.location.lng]
            ]}
            color="blue"
            weight={3}
            opacity={0.7}
          />
        )}
      </MapContainer>

      {/* Doctor Details Drawer */}
      <Drawer
        title="Doctor Details"
        placement="right"
        onClose={() => {
          setDrawerVisible(false)
          setSelectedDoctor(null)
        }}
        open={drawerVisible}
        width={400}
      >
        {selectedDoctor && (
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Title level={4} className="!mb-0">{selectedDoctor.name}</Title>
                <CheckCircleFilled style={{ color: '#1890FF', fontSize: 20 }} />
              </div>
              <Text className="text-gray-600">{selectedDoctor.specialization}</Text>
            </div>

            <div>
              <Text className="text-gray-500 block mb-1">Hospital</Text>
              <Text strong>{selectedDoctor.hospital}</Text>
            </div>

            <div>
              <Text className="text-gray-500 block mb-1">Distance</Text>
              <Text strong>
                {calculateDistance(
                  userLocation.lat,
                  userLocation.lng,
                  selectedDoctor.location.lat,
                  selectedDoctor.location.lng
                )} km away
              </Text>
            </div>

            <div>
              <Text className="text-gray-500 block mb-1">Consultation Fee</Text>
              <Text strong className="text-lg">₹{selectedDoctor.fees}</Text>
            </div>

            <Button
              type="primary"
              size="large"
              block
              onClick={() => navigate(`/patient/book-appointment/${selectedDoctor.id}`)}
            >
              Book Appointment
            </Button>
          </Space>
        )}
      </Drawer>
    </div>
  )
}
