'use client'

import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { useAuthStore } from '@/store/auth-store'
import Link from 'next/link'

const quickActions = [
  { href: '/experiments', label: 'New Experiment', icon: '🔬', desc: 'Create a research experiment' },
  { href: '/datasets', label: 'Upload Dataset', icon: '📊', desc: 'Add a new dataset' },
  { href: '/prompt-lab', label: 'Test Prompt', icon: '🧪', desc: 'Run prompt tests' },
  { href: '/agents', label: 'Run Agent', icon: '🤖', desc: 'Execute AI agents' },
  { href: '/benchmarks', label: 'Benchmark', icon: '📈', desc: 'Compare models' },
]

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)

  return (
    <MainLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Welcome back{user?.username ? `, ${user.username}` : ''}! 👋</h1>
          <p className="text-muted-foreground mt-2">Arvesha Research Platform — AI experimentation at your fingertips.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action) => (
            <Link key={action.href} href={action.href}>
              <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
                <CardHeader>
                  <div className="text-3xl mb-2">{action.icon}</div>
                  <CardTitle className="text-base">{action.label}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{action.desc}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Platform Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Experiments', value: 'Create & manage', icon: '🔬' },
                { label: 'Datasets', value: 'Upload & embed', icon: '📊' },
                { label: 'RAG Pipeline', value: 'Query & stream', icon: '🔍' },
                { label: 'Benchmarks', value: 'Compare models', icon: '📈' },
              ].map((stat) => (
                <div key={stat.label} className="p-4 rounded-lg bg-secondary">
                  <div className="text-2xl mb-1">{stat.icon}</div>
                  <div className="font-medium text-sm">{stat.label}</div>
                  <div className="text-xs text-muted-foreground">{stat.value}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
