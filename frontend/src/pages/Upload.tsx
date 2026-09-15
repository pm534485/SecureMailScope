import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { UploadCloud, File, CheckCircle2, Play, Loader2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import { Button } from "../components/ui/button"

export function UploadPage() {
  const [dragActive, setDragActive] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const navigate = useNavigate()
  
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true)
    else if (e.type === "dragleave") setDragActive(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleStartAnalysis = async () => {
    if (!file) return;
    setUploading(true);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      });
      
      if (response.ok) {
        const data = await response.json();
        // Redirect to a progress/results page, for now just go to dashboard
        setTimeout(() => {
          navigate(`/?analysis_id=${data.analysis_id}`);
        }, 1500);
      } else {
        console.error("Upload failed");
        setUploading(false);
      }
    } catch (error) {
      console.error(error);
      setUploading(false);
    }
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">New Analysis</h1>
        <p className="text-muted-foreground">Upload a PCAP or PCAPNG file containing email traffic.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>File Upload</CardTitle>
          <CardDescription>Max file size 100MB. Processed locally.</CardDescription>
        </CardHeader>
        <CardContent>
          <div 
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors flex flex-col items-center justify-center gap-4 cursor-pointer
              ${dragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50 hover:bg-secondary/50'}
            `}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload')?.click()}
          >
            <input 
              id="file-upload" 
              type="file" 
              className="hidden" 
              accept=".pcap,.pcapng"
              onChange={handleChange}
            />
            
            <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center">
              <UploadCloud className="w-8 h-8 text-primary" />
            </div>
            
            <div>
              <p className="text-lg font-medium">Drop your PCAP or PCAPNG file here</p>
              <p className="text-sm text-muted-foreground mt-1">or click to browse files</p>
            </div>
          </div>

          {file && (
            <div className="mt-6 p-4 border rounded-lg bg-card flex items-center gap-4">
              <div className="p-3 bg-secondary rounded-md">
                <File className="w-6 h-6 text-primary" />
              </div>
              <div className="flex-1">
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <div className="flex items-center gap-2 text-green-400 text-sm font-medium">
                <CheckCircle2 className="w-4 h-4" /> Valid Format
              </div>
            </div>
          )}

          <div className="mt-8 flex justify-end gap-4">
            <Button variant="outline" onClick={() => setFile(null)} disabled={!file || uploading}>Cancel</Button>
            <Button disabled={!file || uploading} onClick={handleStartAnalysis} className="flex items-center gap-2">
              {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />} 
              {uploading ? "Uploading..." : "Start Analysis"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
