import { useState, useEffect } from 'react'
import {
  Card,
  Row,
  Col,
  Typography,
  Button,
  Modal,
  Form,
  Input,
  Select,
  Empty,
  Popconfirm,
  Tag
} from 'antd'
import {
  PlusOutlined,
  DeleteOutlined,
  UserOutlined,
  HistoryOutlined
} from '@ant-design/icons'
import api from '../../services/api'
import toast from 'react-hot-toast'

const { Title, Text } = Typography
const { Option } = Select

interface FamilyMember {
  id: number
  name: string
  age: number
  relationship: string
}

export default function FamilyManagement() {
  const [members, setMembers] = useState<FamilyMember[]>([])
  const [modalVisible, setModalVisible] = useState(false)
  const [form] = Form.useForm()

  useEffect(() => {
    loadFamilyMembers()
  }, [])

  const loadFamilyMembers = async () => {
    try {
      const response = await api.get('/family')
      setMembers(response.data.family_members || [])
    } catch (error) {
      toast.error('Failed to load family members')
    }
  }

  const handleAddMember = async (values: any) => {
    try {
      await api.post('/family', {
        name: values.name,
        age: Number(values.age),
        relationship: values.relationship
      })
      
      toast.success('Family member added successfully')
      setModalVisible(false)
      form.resetFields()
      loadFamilyMembers()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to add family member')
    }
  }

  const handleDeleteMember = async (memberId: number) => {
    try {
      await api.delete(`/family/${memberId}`)
      toast.success('Family member removed')
      loadFamilyMembers()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to remove family member')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <Title level={2} className="!mb-2">Family Health</Title>
            <Text className="text-gray-500">Manage health records for your entire family</Text>
          </div>
          <Button
            type="primary"
            size="large"
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            Add Family Member
          </Button>
        </div>

        {members.length === 0 ? (
          <Card style={{ borderRadius: 12 }}>
            <Empty
              description="No family members added yet"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            >
              <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
                Add Your First Family Member
              </Button>
            </Empty>
          </Card>
        ) : (
          <Row gutter={[16, 16]}>
            {members.map((member) => (
              <Col xs={24} sm={12} lg={8} key={member.id}>
                <Card
                  hoverable
                  style={{ borderRadius: 12 }}
                  actions={[
                    <Button
                      type="text"
                      icon={<HistoryOutlined />}
                      onClick={() => {/* View health history */}}
                    >
                      Health History
                    </Button>,
                    <Popconfirm
                      title="Remove family member?"
                      description="This will remove all their health records"
                      onConfirm={() => handleDeleteMember(member.id)}
                      okText="Yes"
                      cancelText="No"
                    >
                      <Button type="text" danger icon={<DeleteOutlined />}>
                        Remove
                      </Button>
                    </Popconfirm>
                  ]}
                >
                  <div className="text-center">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <UserOutlined style={{ fontSize: 40, color: '#1890FF' }} />
                    </div>
                    <Title level={4} className="!mb-2">{member.name}</Title>
                    <Text className="text-gray-600 block mb-2">{member.age} years old</Text>
                    <Tag color="blue">{member.relationship}</Tag>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
        )}

        {/* Add Family Member Modal */}
        <Modal
          title="Add Family Member"
          open={modalVisible}
          onCancel={() => {
            setModalVisible(false)
            form.resetFields()
          }}
          footer={null}
          width={500}
        >
          <Form
            form={form}
            layout="vertical"
            onFinish={handleAddMember}
            size="large"
          >
            <Form.Item
              name="name"
              label="Full Name"
              rules={[{ required: true, message: 'Please enter name' }]}
            >
              <Input placeholder="Enter full name" />
            </Form.Item>

            <Form.Item
              name="age"
              label="Age"
              rules={[{ required: true, message: 'Please enter age' }]}
            >
              <Input type="number" placeholder="Enter age" min={0} max={120} />
            </Form.Item>

            <Form.Item
              name="relationship"
              label="Relationship"
              rules={[{ required: true, message: 'Please select relationship' }]}
            >
              <Select placeholder="Select relationship">
                <Option value="Spouse">Spouse</Option>
                <Option value="Child">Child</Option>
                <Option value="Parent">Parent</Option>
                <Option value="Sibling">Sibling</Option>
                <Option value="Grandparent">Grandparent</Option>
                <Option value="Other">Other</Option>
              </Select>
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" block>
                Add Family Member
              </Button>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    </div>
  )
}
