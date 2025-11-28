import React from 'react'

function UploadForm(){
  const [file, setFile] = React.useState(null)
  const [transcript, setTranscript] = React.useState(null)

  const upload = async () =>{
    if(!file) return
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch('http://localhost:8000/api/transcribe', {method: 'POST', body: fd})
    const json = await res.json()
    setTranscript(json.transcript)
  }

  return (
    <div style={{padding:20}}>
      <h1>Smart Meeting Assistant (MVP)</h1>
      <input type="file" accept="audio/*" onChange={(e)=>setFile(e.target.files[0])} />
      <button onClick={upload}>Upload & Transcribe</button>
      {transcript && (
        <div style={{marginTop:20}}>
          <h3>Transcript</h3>
          <pre>{transcript.text || JSON.stringify(transcript, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default function App(){ return <UploadForm /> }
