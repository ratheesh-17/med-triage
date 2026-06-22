import { Card, Form, InputNumber, Button, Select, Tag, Input, Switch, Typography, message, Row, Col } from 'antd'
import { PlusOutlined, SaveOutlined } from '@ant-design/icons'
import { useState } from 'react'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input

const INITIAL_SPECIALIZATIONS = [
  'General Physician', 'Cardiologist', 'Dermatologist', 'Pediatrician', 'Orthopedic',
  'Gynecologist', 'Neurologist', 'Psychiatrist', 'ENT Specialist', 'Ophthalmologist'
]

export default function PlatformSettings() {
  const [form] = Form.useForm()
  const [specializations, setSpecializations] = useState(INITIAL_SPECIALIZATIONS)
  const [newSpecialization, setNewSpecialization] = useState('')
  const [disclaimerFrequency, setDisclaimerFrequency] = useState('first-use')

  const handleSave = (values: any) => {
    console.log('Settings saved:', values)
    message.success('Platform settings updated successfully')
  }

  const addSpecialization = () => {
    if (newSpecialization.trim() && !specializations.includes(newSpecialization.trim())) {
      setSpecializations([...specializations, newSpecialization.trim()])
      setNewSpecialization('')
      message.success('Specialization added')
    }
  }

  const removeSpecialization = (spec: string) => {
    setSpecializations(specializations.filter(s => s !== spec))
    message.success('Specialization removed')
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <Title level={2} className="mb-6">Platform Settings</Title>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            emergencyThreshold: 9,
            outbreakThreshold: 15,
            disclaimerText: 'This AI-powered symptom analysis is for informational purposes only and does not replace professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.'
          }}
        >
          {/* Emergency & Outbreak Settings */}
          <Card title="Emergency & Outbreak Detection" className="mb-6 shadow-sm">
            <Row gutter={16}>
              <Col xs={24} md={12}>
                <Form.Item
                  name="emergencyThreshold"
                  label="Emergency Severity Threshold"
                  help="AI severity score at which emergency mode activates"
                >
                  <InputNumber min={1} max={10} className="w-full" />
                </Form.Item>
              </Col>
              <Col xs={24} md={12}>
                <Form.Item
                  name="outbreakThreshold"
                  label="Outbreak Detection Threshold"
                  help="Minimum case count in a region within 7 days to trigger watch alert"
                >
                  <InputNumber min={5} max={50} className="w-full" />
                </Form.Item>
              </Col>
            </Row>
          </Card>

          {/* Specializations Management */}
          <Card title="Medical Specializations" className="mb-6 shadow-sm">
            <div className="mb-4">
              <Text className="block mb-2">Current Specializations:</Text>
              <div className="flex flex-wrap gap-2 mb-4">
                {specializations.map(spec => (
                  <Tag
                    key={spec}
                    closable
                    onClose={() => removeSpecialization(spec)}
                    color="blue"
                  >
                    {spec}
                  </Tag>
                ))}
              </div>
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Add new specialization"
                value={newSpecialization}
                onChange={(e) => setNewSpecialization(e.target.value)}
                onPressEnter={addSpecialization}
              />
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={addSpecialization}
              >
                Add
              </Button>
            </div>
          </Card>

          {/* Responsible AI Settings */}
          <Card title="Responsible AI Settings" className="mb-6 shadow-sm">
            <Form.Item
              name="disclaimerText"
              label="AI Disclaimer Text"
              help="Shown to patients when using AI symptom analysis"
            >
              <TextArea rows={4} maxLength={500} showCount />
            </Form.Item>

            <div className="mb-4">
              <Text strong className="block mb-2">Disclaimer Display Frequency</Text>
              <Select
                value={disclaimerFrequency}
                onChange={setDisclaimerFrequency}
                className="w-full"
              >
                <Select.Option value="first-use">Show only on first use</Select.Option>
                <Select.Option value="every-session">Show before every AI session</Select.Option>
                <Select.Option value="daily">Show once per day</Select.Option>
              </Select>
            </div>

            <Card size="small" className="bg-blue-50 border-blue-300">
              <Text strong className="block mb-2">Ethical AI Governance</Text>
              <Paragraph className="!mb-0 text-sm">
                These settings ensure transparent and responsible use of AI in medical triage. 
                All AI recommendations are clearly labeled as non-diagnostic and patients are 
                encouraged to seek professional medical advice.
              </Paragraph>
            </Card>
          </Card>

          {/* Platform Maintenance */}
          <Card title="Platform Maintenance" className="mb-6 shadow-sm">
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <Text strong className="block">Maintenance Mode</Text>
                  <Text className="text-sm text-gray-600">Temporarily disable patient/doctor access</Text>
                </div>
                <Switch />
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <Text strong className="block">New Doctor Registrations</Text>
                  <Text className="text-sm text-gray-600">Allow new doctors to register</Text>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <Text strong className="block">AI Service</Text>
                  <Text className="text-sm text-gray-600">Enable AI symptom analysis</Text>
                </div>
                <Switch defaultChecked />
              </div>
            </div>
          </Card>

          {/* Save Button */}
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SaveOutlined />}
              size="large"
              block
            >
              Save All Settings
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  )
}
