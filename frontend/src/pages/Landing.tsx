import { Shield, Upload, FileText, Brain, Activity } from "lucide-react"
import { Link } from "react-router-dom"
import { Button } from "../components/ui/button"

export function Landing() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <header className="px-8 py-6 flex items-center justify-between border-b border-border">
        <div className="flex items-center gap-3">
          <Shield className="w-8 h-8 text-primary" />
          <span className="font-bold text-2xl tracking-tight">SecureMailScope</span>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center p-8 max-w-5xl mx-auto text-center">
        <h1 className="text-5xl font-extrabold tracking-tight mb-6">
          Analyze email network captures.<br/>
          <span className="text-primary">Discover cryptographic weaknesses. Prioritize risk.</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-10 max-w-2xl">
          An AI-assisted cryptographic security posture assessment framework for passive network forensics on SMTP, IMAP, and POP3 communications.
        </p>

        <div className="flex items-center gap-4 mb-16">
          <Button size="lg" asChild>
            <Link to="/upload" className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload PCAP
            </Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link to="/" className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Try Demo Analysis
            </Link>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 w-full text-left">
          <FeatureCard 
            icon={Shield} 
            title="Passive PCAP Analysis" 
            desc="Extract TCP streams and detect STARTTLS/STLS upgrades without active connection."
          />
          <FeatureCard 
            icon={FileText} 
            title="TLS & Certificate Intelligence" 
            desc="Reconstruct handshakes, identify weak ciphers, and assess X.509 validity."
          />
          <FeatureCard 
            icon={Brain} 
            title="AI-Assisted Risk Detection" 
            desc="Supervised risk classification and unsupervised TLS anomaly detection."
          />
          <FeatureCard 
            icon={Activity} 
            title="Explainable Security Findings" 
            desc="Evidence-to-impact reasoning with clear remediation recommendations."
          />
        </div>
        
        <p className="mt-16 text-sm text-muted-foreground">
          PCAP files may contain sensitive network metadata. Process captures locally whenever possible.
        </p>
      </main>
    </div>
  )
}

function FeatureCard({ icon: Icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="p-6 rounded-xl border border-border bg-card/50 flex flex-col gap-4">
      <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="font-semibold text-lg">{title}</h3>
      <p className="text-muted-foreground text-sm leading-relaxed">{desc}</p>
    </div>
  )
}
