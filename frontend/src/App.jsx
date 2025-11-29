import React from 'react'

function UploadForm(){
  const [file, setFile] = React.useState(null)
  const [transcript, setTranscript] = React.useState(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  const upload = async () =>{
    if(!file) {
      setError('Please select a file first')
      return
    }
    
    setLoading(true)
    setError(null)
    setTranscript(null)
    
    try {
      const fd = new FormData()
      fd.append('file', file)
      
      const res = await fetch('http://localhost:8000/api/transcribe_and_analyze', {
        method: 'POST', 
        body: fd
      })
      
      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || `HTTP error! status: ${res.status}`)
      }
      
      const json = await res.json()
      
      if (json.error) {
        throw new Error(json.error)
      }
      
      setTranscript(json)
    } catch (err) {
      setError(err.message || 'Failed to transcribe audio')
      console.error('Upload error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{padding:20, maxWidth: 800, margin: '0 auto'}}>
      <h1>Smart Meeting Assistant (MVP)</h1>
      
      <div style={{marginTop: 20}}>
        <input 
          type="file" 
          accept="audio/*,video/*" 
          onChange={(e)=>{
            setFile(e.target.files[0])
            setError(null)
          }} 
          disabled={loading}
        />
        <button 
          onClick={upload} 
          disabled={loading || !file}
          style={{
            marginLeft: 10,
            padding: '8px 16px',
            cursor: loading || !file ? 'not-allowed' : 'pointer',
            opacity: loading || !file ? 0.6 : 1
          }}
        >
          {loading ? 'Processing...' : 'Upload & Transcribe'}
        </button>
      </div>
      
      {loading && (
        <div style={{marginTop:20, color: '#0066cc'}}>
          <p>⏳ Transcribing audio... This may take a few minutes.</p>
        </div>
      )}
      
      {error && (
        <div style={{marginTop:20, padding: 15, backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: 4}}>
          <h3 style={{color: '#c00', margin: '0 0 10px 0'}}>Error</h3>
          <p style={{margin: 0}}>{error}</p>
        </div>
      )}
      
      {transcript && (
        <div style={{marginTop:20, padding: 15, backgroundColor: '#efe', border: '1px solid #cfc', borderRadius: 4}}>
          <h3 style={{margin: '0 0 10px 0'}}>Transcript</h3>
          <pre style={{
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word',
            backgroundColor: 'white',
            padding: 10,
            borderRadius: 4,
            maxHeight: 400,
            overflow: 'auto'
          }}>
            {transcript.transcript || JSON.stringify(transcript, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

export default function App(){ return <UploadForm /> }
