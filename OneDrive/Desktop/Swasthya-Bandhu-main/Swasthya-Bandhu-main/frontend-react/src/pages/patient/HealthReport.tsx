import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Typography, Button, Divider, Tag, Space, Spin } from 'antd'
import { DownloadOutlined, ShareAltOutlined } from '@ant-design/icons'
import api from '../../services/api'
import toast from 'react-hot-toast'
import dayjs from 'dayjs'

const { Title, Text, Paragraph } = Typography

export default function HealthReport() {
  const { sessionId } = useParams()
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReport()
  }, [sessionId])

  const loadReport = async () => {
    setLoading(true)
    try {
      // Mock data - replace with actual API call
      setReport({
        id: sessionId,
        patient_name: 'John Doe',
        age: 30,
        gender: 'Male',
        date: '2024-02-22',
        time: '10:30 AM',
        symptom_input: 'I have been experiencing severe headaches and dizziness for the past 3 days',
        severity_score: 7,
        urgency: 'within 24 hours',
        recommended_specialist: 'Neurologist',
        risk_factors: ['Neurological symptoms', 'Persistent headache', 'Dizziness'],
        suggested_tests: ['CT scan', 'MRI', 'Blood pressure monitoring'],
        differential_diagnoses: ['Migraine', 'Tension headache', 'Hypertension']
      })
    } catch (error) {
      toast.error('Failed to load report')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    try {
      await api.get(`/session/${sessionId}/report`)
      toast.success('Report downloaded successfully')
    } catch (error) {
      toast.error('Failed to download report')
    }
  }

  const handleShare = () => {
    toast.success('Share feature coming soon')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Spin size="large" />
      </div>
    )
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card>
          <Text>Report not found</Text>
        </Card>
      </div>
    )
  }

  const getSeverityColor = (score: number) => {
    if (score >= 9) return 'red'
    if (score >= 7) return 'orange'
    if (score >= 5) return 'gold'
    return 'green'
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header Actions */}
        <div className="flex justify-between items-center mb-6">
          <Title level={2} className="!mb-0">Health Assessment Report</Title>
          <Space>
            <Button icon={<ShareAltOutlined />} onClick={handleShare}>
              Share with Doctor
            </Button>
            <Button type="primary" icon={<DownloadOutlined />} onClick={handleDownloadPDF}>
              Download PDF
            </Button>
          </Space>
        </div>

        {/* Report Card */}
        <Card style={{ borderRadius: 12 }}>
          {/* Patient Information */}
          <div className="mb-6">
            <Title level={4} className="!mb-4">Patient Information</Title>
            <Space direction="vertical" size="small">
              <Text><strong>Name:</strong> {report.patient_name}</Text>
              <Text><strong>Age:</strong> {report.age} years</Text>
              <Text><strong>Gender:</strong> {report.gender}</Text>
              <Text><strong>Date:</strong> {dayjs(report.date).format('DD MMM YYYY')} at {report.time}</Text>
            </Space>
          </div>

          <Divider />

          {/* Symptoms Described */}
          <div className="mb-6">
            <Title level={4} className="!mb-4">Symptoms Described</Title>
            <Paragraph className="bg-gray-50 p-4 rounded">
              {report.symptom_input}
            </Paragraph>
          </div>

          <Divider />

          {/* Assessment Results */}
          <div className="mb-6">
            <Title level={4} className="!mb-4">Assessment Results</Title>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-blue-50 p-4 rounded">
                <Text className="text-gray-600 block mb-1">Severity Score</Text>
                <div className="flex items-center gap-2">
                  <Title level={2} className="!mb-0">{report.severity_score}/10</Title>
                  <Tag color={getSeverityColor(report.severity_score)}>
                    {report.severity_score >= 7 ? 'High' : report.severity_score >= 5 ? 'Moderate' : 'Low'}
                  </Tag>
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded">
                <Text className="text-gray-600 block mb-1">Urgency</Text>
                <Title level={4} className="!mb-0 !mt-2">{report.urgency}</Title>
              </div>
            </div>

            <div className="bg-indigo-50 p-4 rounded">
              <Text className="text-gray-600 block mb-2">Recommended Specialist</Text>
              <Title level={4} className="!mb-0 text-blue-600">{report.recommended_specialist}</Title>
            </div>
          </div>

          <Divider />

          {/* Risk Factors */}
          {report.risk_factors?.length > 0 && (
            <div className="mb-6">
              <Title level={4} className="!mb-4">Identified Risk Factors</Title>
              <ul className="list-disc pl-6">
                {report.risk_factors.map((factor: string, i: number) => (
                  <li key={i} className="mb-2">
                    <Text>{factor}</Text>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Suggested Tests */}
          {report.suggested_tests?.length > 0 && (
            <div className="mb-6">
              <Title level={4} className="!mb-4">Suggested Diagnostic Tests</Title>
              <Space wrap>
                {report.suggested_tests.map((test: string, i: number) => (
                  <Tag key={i} color="blue" className="!py-1 !px-3">
                    {test}
                  </Tag>
                ))}
              </Space>
            </div>
          )}

          {/* Differential Diagnoses */}
          {report.differential_diagnoses?.length > 0 && (
            <div className="mb-6">
              <Title level={4} className="!mb-4">Possible Conditions (Differential Diagnoses)</Title>
              <ul className="list-disc pl-6">
                {report.differential_diagnoses.map((diagnosis: string, i: number) => (
                  <li key={i} className="mb-2">
                    <Text>{diagnosis}</Text>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <Divider />

          {/* Disclaimer */}
          <div className="bg-yellow-50 p-4 rounded">
            <Text strong className="block mb-2">⚠️ Important Disclaimer</Text>
            <Paragraph className="!mb-0 text-sm text-gray-700">
              This is an AI-powered triage assessment and <strong>not a medical diagnosis</strong>. 
              The information provided is for preliminary assessment purposes only. Please consult 
              a qualified healthcare professional for proper medical advice, diagnosis, and treatment. 
              Do not rely solely on this assessment for medical decisions.
            </Paragraph>
          </div>
        </Card>
      </div>
    </div>
  )
}
