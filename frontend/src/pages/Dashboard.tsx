import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import { Badge } from "../components/ui/badge"
import { Button } from "../components/ui/button"
import { AlertTriangle, Info, ShieldAlert } from "lucide-react"

export function Dashboard() {
  return (
    <div className="p-8 space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Security Dashboard</h1>
        <Badge variant="outline" className="px-3 py-1 text-sm bg-primary/10 text-primary border-primary/20">
          DEMO DATA
        </Badge>
      </div>

      {/* Top Section */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="col-span-1 md:col-span-1 bg-card">
          <CardHeader className="pb-2">
            <CardDescription>Overall Security Score</CardDescription>
            <CardTitle className="text-5xl font-extrabold text-green-400">
              78 <span className="text-xl font-normal text-muted-foreground">/ 100</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="success">GOOD</Badge>
              <span className="text-sm text-muted-foreground">91% Confidence</span>
            </div>
          </CardContent>
        </Card>

        <div className="col-span-1 md:col-span-3 grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard title="Email Sessions" value="1,245" />
          <StatCard title="TLS Sessions" value="1,102" />
          <StatCard title="Certificates" value="48" />
          <StatCard title="Critical Findings" value="2" alert />
          <StatCard title="High Findings" value="5" warning />
          <StatCard title="Medium Findings" value="12" />
          <StatCard title="Low Findings" value="34" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2 border-b pb-2">
            <ShieldAlert className="w-5 h-5 text-orange-400" />
            What Needs Attention?
          </h2>
          <div className="space-y-4">
            <FindingCard 
              severity="HIGH"
              title="Deprecated TLS Version"
              protocol="SMTP"
              desc="SMTP session negotiated TLS 1.0 which is deprecated and vulnerable."
              score="85"
            />
            <FindingCard 
              severity="CRITICAL"
              title="Expired Certificate"
              protocol="IMAP"
              desc="IMAP server presented an expired X.509 certificate."
              score="95"
            />
          </div>
        </div>

        <div className="space-y-6">
          <h2 className="text-xl font-semibold border-b pb-2">Security Posture</h2>
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Protocol Distribution</CardTitle>
            </CardHeader>
            <CardContent className="h-48 flex items-center justify-center text-muted-foreground">
              [Chart Placeholder]
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, alert, warning }: { title: string, value: string, alert?: boolean, warning?: boolean }) {
  return (
    <Card className="flex flex-col justify-center px-6 py-4">
      <span className="text-sm text-muted-foreground font-medium">{title}</span>
      <span className={`text-2xl font-bold mt-1 ${alert ? 'text-destructive' : warning ? 'text-orange-400' : ''}`}>
        {value}
      </span>
    </Card>
  )
}

function FindingCard({ severity, title, protocol, desc, score }: any) {
  return (
    <Card className="hover:border-primary/50 transition-colors">
      <div className="p-5 flex items-start gap-4">
        <div className="mt-1">
          {severity === 'CRITICAL' ? <AlertTriangle className="w-5 h-5 text-destructive" /> : 
           severity === 'HIGH' ? <AlertTriangle className="w-5 h-5 text-orange-400" /> : 
           <Info className="w-5 h-5 text-blue-400" />}
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <Badge variant={severity === 'CRITICAL' ? 'destructive' : severity === 'HIGH' ? 'warning' : 'secondary'}>
              {severity}
            </Badge>
            <h3 className="font-semibold">{title}</h3>
            <Badge variant="outline" className="ml-auto">{protocol}</Badge>
          </div>
          <p className="text-sm text-muted-foreground">{desc}</p>
          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-muted-foreground">Risk Score: {score}/100</span>
            <Button variant="outline" size="sm">View Evidence</Button>
          </div>
        </div>
      </div>
    </Card>
  )
}
