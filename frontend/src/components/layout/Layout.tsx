import { Link, Outlet, useLocation } from "react-router-dom"
import { Shield, LayoutDashboard, Search, FileText, Activity, Layers, FileCheck, Settings, HelpCircle, ActivitySquare } from "lucide-react"

const navItems = [
  { name: "Overview", href: "/", icon: LayoutDashboard },
  { name: "New Analysis", href: "/upload", icon: Search },
  { name: "Sessions", href: "/sessions", icon: Layers },
  { name: "Findings", href: "/findings", icon: FileText },
  { name: "Certificates", href: "/certificates", icon: FileCheck },
  { name: "TLS Intelligence", href: "/tls", icon: Shield },
  { name: "AI Intelligence", href: "/ai", icon: ActivitySquare },
  { name: "Posture Trends", href: "/trends", icon: Activity },
  { name: "Reports", href: "/reports", icon: FileText },
]

export function Layout() {
  const location = useLocation()

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <div className="w-64 border-r border-border bg-card/50 flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <Shield className="w-8 h-8 text-primary" />
          <span className="font-bold text-xl tracking-tight">SecureMailScope</span>
        </div>
        <nav className="flex-1 overflow-y-auto px-4 py-2 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.href || 
                             (item.href !== "/" && location.pathname.startsWith(item.href))
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                  isActive 
                    ? "bg-primary/10 text-primary font-medium" 
                    : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>
        <div className="p-4 border-t border-border space-y-1">
          <Link to="/settings" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors">
            <Settings className="w-5 h-5" />
            Settings
          </Link>
          <Link to="/help" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors">
            <HelpCircle className="w-5 h-5" />
            Help
          </Link>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 overflow-y-auto bg-background">
        <Outlet />
      </div>
    </div>
  )
}
