import { useState, useEffect } from 'react'
import { Card, Table, Button, Popconfirm, message, Tabs, Tag, Typography } from 'antd'
import { DeleteOutlined, UserOutlined, MedicineBoxOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title } = Typography
const { TabPane } = Tabs

export default function UserManagement() {
  const [users, setUsers] = useState<any[]>([])
  const [doctors, setDoctors] = useState<any[]>([])
  const [loadingUsers, setLoadingUsers] = useState(true)
  const [loadingDoctors, setLoadingDoctors] = useState(true)

  useEffect(() => {
    fetchUsers()
    fetchDoctors()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await api.get('/admin/users')
      setUsers(response.data.users)
    } catch (error) {
      message.error('Failed to fetch users')
    } finally {
      setLoadingUsers(false)
    }
  }

  const fetchDoctors = async () => {
    try {
      const response = await api.get('/admin/doctors')
      setDoctors(response.data.doctors)
    } catch (error) {
      message.error('Failed to fetch doctors')
    } finally {
      setLoadingDoctors(false)
    }
  }

  const handleDeleteUser = async (userId: number) => {
    try {
      await api.delete(`/admin/users/${userId}`)
      message.success('User deleted successfully')
      fetchUsers()
    } catch (error) {
      message.error('Failed to delete user')
    }
  }

  const handleDeleteDoctor = async (doctorId: number) => {
    try {
      await api.delete(`/admin/doctors/${doctorId}`)
      message.success('Doctor deleted successfully')
      fetchDoctors()
    } catch (error) {
      message.error('Failed to delete doctor')
    }
  }

  const userColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Phone', dataIndex: 'phone', key: 'phone' },
    { title: 'Age', dataIndex: 'age', key: 'age', width: 80 },
    { title: 'Gender', dataIndex: 'gender', key: 'gender', width: 100 },
    {
      title: 'Registered',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString()
    },
    {
      title: 'Action',
      key: 'action',
      width: 100,
      render: (_: any, record: any) => (
        <Popconfirm
          title="Delete this user?"
          description="This will permanently delete the user and all related data."
          onConfirm={() => handleDeleteUser(record.id)}
          okText="Delete"
          cancelText="Cancel"
          okButtonProps={{ danger: true }}
        >
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      )
    }
  ]

  const doctorColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Phone', dataIndex: 'phone', key: 'phone' },
    { title: 'Specialization', dataIndex: 'specialization', key: 'specialization' },
    { title: 'Hospital', dataIndex: 'hospital', key: 'hospital' },
    { title: 'Experience', dataIndex: 'experience', key: 'experience', width: 100 },
    { title: 'Fees', dataIndex: 'fees', key: 'fees', width: 100, render: (fees: number) => `₹${fees}` },
    {
      title: 'Status',
      dataIndex: 'verification_status',
      key: 'verification_status',
      width: 120,
      render: (status: string) => (
        <Tag color={status === 'approved' ? 'green' : status === 'pending' ? 'orange' : 'red'}>
          {status.toUpperCase()}
        </Tag>
      )
    },
    {
      title: 'Active',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 80,
      render: (active: boolean) => <Tag color={active ? 'green' : 'red'}>{active ? 'Yes' : 'No'}</Tag>
    },
    {
      title: 'Registered',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString()
    },
    {
      title: 'Action',
      key: 'action',
      width: 100,
      render: (_: any, record: any) => (
        <Popconfirm
          title="Delete this doctor?"
          description="This will permanently delete the doctor and all related data."
          onConfirm={() => handleDeleteDoctor(record.id)}
          okText="Delete"
          cancelText="Cancel"
          okButtonProps={{ danger: true }}
        >
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      )
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <Title level={2}>User Management</Title>

        <Tabs defaultActiveKey="users">
          <TabPane
            tab={
              <span>
                <UserOutlined />
                Patients ({users.length})
              </span>
            }
            key="users"
          >
            <Card>
              <Table
                columns={userColumns}
                dataSource={users}
                rowKey="id"
                loading={loadingUsers}
                pagination={{ pageSize: 10 }}
              />
            </Card>
          </TabPane>

          <TabPane
            tab={
              <span>
                <MedicineBoxOutlined />
                Doctors ({doctors.length})
              </span>
            }
            key="doctors"
          >
            <Card>
              <Table
                columns={doctorColumns}
                dataSource={doctors}
                rowKey="id"
                loading={loadingDoctors}
                pagination={{ pageSize: 10 }}
                scroll={{ x: 1200 }}
              />
            </Card>
          </TabPane>
        </Tabs>
      </div>
    </div>
  )
}
