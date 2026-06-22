import { useState } from 'react'
import { Card, Calendar, Button, Modal, Form, Select, TimePicker, Row, Col, Typography, Tag } from 'antd'
import { ClockCircleOutlined, LockOutlined, CheckCircleOutlined } from '@ant-design/icons'
import dayjs, { Dayjs } from 'dayjs'
import toast from 'react-hot-toast'

const { Title, Text } = Typography
const { RangePicker } = TimePicker

interface Slot {
  time: string
  status: string
  patient?: string
}

interface SlotsData {
  [key: string]: Slot[]
}

const MOCK_SLOTS: SlotsData = {
  '2024-01-15': [
    { time: '09:00', status: 'available' },
    { time: '09:30', status: 'booked', patient: 'Rajesh Kumar' },
    { time: '10:00', status: 'available' },
    { time: '10:30', status: 'blocked' },
    { time: '11:00', status: 'booked', patient: 'Priya Sharma' },
    { time: '14:00', status: 'available' },
    { time: '14:30', status: 'available' },
    { time: '15:00', status: 'booked', patient: 'Amit Patel' }
  ]
}

export default function SlotManagement() {
  const [selectedDate, setSelectedDate] = useState<Dayjs>(dayjs())
  const [recurringModal, setRecurringModal] = useState(false)
  const [leaveModal, setLeaveModal] = useState(false)
  const [slots, setSlots] = useState<SlotsData>(MOCK_SLOTS)

  const getDateSlots = (date: Dayjs) => {
    return slots[date.format('YYYY-MM-DD')] || []
  }

  const dateCellRender = (date: Dayjs) => {
    const dateSlots = getDateSlots(date)
    const available = dateSlots.filter((s: Slot) => s.status === 'available').length
    const booked = dateSlots.filter((s: Slot) => s.status === 'booked').length
    
    if (dateSlots.length === 0) return null
    
    return (
      <div className="text-xs">
        <div className="text-green-600">{available} avail</div>
        <div className="text-blue-600">{booked} booked</div>
      </div>
    )
  }

  const toggleSlotStatus = (time: string) => {
    const dateKey = selectedDate.format('YYYY-MM-DD')
    const dateSlots = slots[dateKey] || []
    const slot = dateSlots.find((s: Slot) => s.time === time)
    
    if (slot && slot.status !== 'booked') {
      const newStatus = slot.status === 'available' ? 'blocked' : 'available'
      const updatedSlots = dateSlots.map((s: Slot) => 
        s.time === time ? { ...s, status: newStatus } : s
      )
      setSlots({ ...slots, [dateKey]: updatedSlots })
      toast.success(`Slot ${newStatus === 'blocked' ? 'blocked' : 'made available'}`)
    }
  }

  const handleRecurringSchedule = (values: any) => {
    console.log('Recurring schedule:', values)
    toast.success('Recurring schedule set for next 30 days')
    setRecurringModal(false)
  }

  const handleBlockLeave = (values: any) => {
    console.log('Leave blocked:', values)
    toast.success('Leave period blocked successfully')
    setLeaveModal(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <Title level={2}>Slot Management</Title>
            <Text className="text-gray-500">Manage your availability and schedule</Text>
          </div>
          <div className="space-x-2">
            <Button type="primary" onClick={() => setRecurringModal(true)}>
              Set Recurring Schedule
            </Button>
            <Button onClick={() => setLeaveModal(true)}>
              Block Leave
            </Button>
          </div>
        </div>

        <Row gutter={16}>
          <Col xs={24} lg={14}>
            <Card title="Monthly Calendar" className="shadow-sm">
              <Calendar 
                fullscreen={false}
                dateCellRender={dateCellRender}
                onSelect={setSelectedDate}
              />
            </Card>
          </Col>

          <Col xs={24} lg={10}>
            <Card 
              title={`Schedule for ${selectedDate.format('DD MMM YYYY')}`}
              className="shadow-sm"
            >
              <div className="space-y-2 max-h-[500px] overflow-y-auto">
                {getDateSlots(selectedDate).length === 0 ? (
                  <div className="text-center py-8 text-gray-400">
                    <ClockCircleOutlined style={{ fontSize: 48 }} />
                    <p className="mt-4">No slots configured for this day</p>
                  </div>
                ) : (
                  getDateSlots(selectedDate).map((slot: Slot) => (
                    <div
                      key={slot.time}
                      className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                        slot.status === 'available' 
                          ? 'border-green-300 bg-green-50 hover:border-green-500' 
                          : slot.status === 'booked'
                          ? 'border-blue-300 bg-blue-50 cursor-not-allowed'
                          : 'border-gray-300 bg-gray-50 hover:border-gray-500'
                      }`}
                      onClick={() => slot.status !== 'booked' && toggleSlotStatus(slot.time)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          {slot.status === 'available' && <CheckCircleOutlined className="text-green-600 text-xl" />}
                          {slot.status === 'booked' && <ClockCircleOutlined className="text-blue-600 text-xl" />}
                          {slot.status === 'blocked' && <LockOutlined className="text-gray-600 text-xl" />}
                          <div>
                            <Text strong className="text-lg">{slot.time}</Text>
                            {slot.patient && (
                              <div className="text-sm text-gray-600">{slot.patient}</div>
                            )}
                          </div>
                        </div>
                        <Tag color={
                          slot.status === 'available' ? 'green' :
                          slot.status === 'booked' ? 'blue' : 'default'
                        }>
                          {slot.status.toUpperCase()}
                        </Tag>
                      </div>
                    </div>
                  ))
                )}
              </div>
              
              <div className="mt-4 pt-4 border-t">
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-green-200 rounded"></div>
                    <Text>Available</Text>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-blue-200 rounded"></div>
                    <Text>Booked</Text>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-gray-200 rounded"></div>
                    <Text>Blocked</Text>
                  </div>
                </div>
              </div>
            </Card>
          </Col>
        </Row>
      </div>

      {/* Recurring Schedule Modal */}
      <Modal
        title="Set Recurring Schedule"
        open={recurringModal}
        onCancel={() => setRecurringModal(false)}
        footer={null}
      >
        <Form layout="vertical" onFinish={handleRecurringSchedule}>
          <Form.Item name="days" label="Days of Week" rules={[{ required: true }]}>
            <Select mode="multiple" placeholder="Select days">
              <Select.Option value="monday">Monday</Select.Option>
              <Select.Option value="tuesday">Tuesday</Select.Option>
              <Select.Option value="wednesday">Wednesday</Select.Option>
              <Select.Option value="thursday">Thursday</Select.Option>
              <Select.Option value="friday">Friday</Select.Option>
              <Select.Option value="saturday">Saturday</Select.Option>
              <Select.Option value="sunday">Sunday</Select.Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="morningSlots" label="Morning Slots">
            <RangePicker format="HH:mm" />
          </Form.Item>
          
          <Form.Item name="afternoonSlots" label="Afternoon Slots">
            <RangePicker format="HH:mm" />
          </Form.Item>
          
          <Form.Item name="eveningSlots" label="Evening Slots">
            <RangePicker format="HH:mm" />
          </Form.Item>
          
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Apply for Next 30 Days
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* Block Leave Modal */}
      <Modal
        title="Block Leave Period"
        open={leaveModal}
        onCancel={() => setLeaveModal(false)}
        footer={null}
      >
        <Form layout="vertical" onFinish={handleBlockLeave}>
          <Form.Item name="dateRange" label="Leave Period" rules={[{ required: true }]}>
            <Calendar fullscreen={false} />
          </Form.Item>
          
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Block All Slots
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}
