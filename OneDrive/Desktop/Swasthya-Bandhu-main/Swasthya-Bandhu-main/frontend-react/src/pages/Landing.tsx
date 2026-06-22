import { Link } from 'react-router-dom'
import { Activity, Brain, Calendar, Shield, Users, TrendingUp, ArrowRight, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import { Card, Row, Col, Typography, Button } from 'antd'

const { Title, Paragraph } = Typography

export default function Landing() {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Diagnosis',
      description: 'Advanced AI analyzes your symptoms and provides instant clinical assessment with severity scoring.',
    },
    {
      icon: Calendar,
      title: 'Smart Appointments',
      description: 'Book appointments with verified doctors based on AI recommendations and proximity.',
    },
    {
      icon: TrendingUp,
      title: 'Health Tracking',
      description: 'Longitudinal health risk analysis tracks your wellness trends over time.',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your health data is encrypted and protected with industry-standard security.',
    },
    {
      icon: Users,
      title: 'Family Management',
      description: 'Manage health records and appointments for your entire family in one place.',
    },
    {
      icon: Activity,
      title: 'Real-time Monitoring',
      description: 'Outbreak detection and health analytics for proactive care management.',
    },
  ]

  const stats = [
    { value: '10K+', label: 'Active Patients' },
    { value: '500+', label: 'Verified Doctors' },
    { value: '50K+', label: 'Consultations' },
    { value: '98%', label: 'Satisfaction Rate' },
  ]

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-28">
          <Row gutter={[48, 24]} align="middle">
            <Col xs={24} lg={12}>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
                <Title style={{ fontSize: '2.75rem' }} className="mb-4">Your AI-Powered <span className="text-primary-600">Healthcare Companion</span></Title>
                <Paragraph className="text-lg text-slate-700 mb-6">Get instant AI-driven health assessments, connect with verified doctors, and manage your family's health—all in one intelligent platform.</Paragraph>
                <div className="flex gap-4">
                  <Link to="/register">
                    <Button type="primary" size="large">Get Started Free</Button>
                  </Link>
                  <Link to="/login">
                    <Button type="default" size="large">Sign In</Button>
                  </Link>
                </div>
              </motion.div>
            </Col>

            <Col xs={24} lg={12}>
              <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, delay: 0.2 }}>
                <Card bordered={false} style={{ borderRadius: 12 }}>
                  <div className="absolute -top-4 -right-4 bg-secondary-500 text-white px-4 py-2 rounded-lg font-semibold shadow-md">AI-Powered</div>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3 p-4 bg-primary-50 rounded-lg">
                      <CheckCircle className="h-6 w-6 text-primary-600" />
                      <span className="font-medium text-slate-700">Instant Symptom Analysis</span>
                    </div>
                    <div className="flex items-center space-x-3 p-4 bg-secondary-50 rounded-lg">
                      <CheckCircle className="h-6 w-6 text-secondary-600" />
                      <span className="font-medium text-slate-700">Smart Doctor Matching</span>
                    </div>
                    <div className="flex items-center space-x-3 p-4 bg-accent-50 rounded-lg">
                      <CheckCircle className="h-6 w-6 text-accent-600" />
                      <span className="font-medium text-slate-700">Health Risk Tracking</span>
                    </div>
                  </div>
                </Card>
              </motion.div>
            </Col>
          </Row>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-slate-900 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="text-4xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-slate-400">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">
              Comprehensive Healthcare Platform
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Everything you need for intelligent health management in one place
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-200 group"
              >
                <div className="bg-gradient-to-br from-primary-500 to-secondary-500 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary-600 to-secondary-600 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Healthcare Experience?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of patients already using AI-powered healthcare
          </p>
          <Link
            to="/register"
            className="inline-flex items-center px-8 py-4 text-lg font-semibold text-primary-600 bg-white rounded-xl hover:bg-slate-50 transition-all duration-200 shadow-hard group"
          >
            Start Your Journey
            <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </section>
    </div>
  )
}
