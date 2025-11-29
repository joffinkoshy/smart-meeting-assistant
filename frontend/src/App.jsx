import React, { useState, useRef } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [segments, setSegments] = useState([]);
  const [intelligence, setIntelligence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] ?? null);
    setError(null);
    setTranscript("");
    setSegments([]);
    setIntelligence(null);
  };

  const reset = () => {
    setFile(null);
    setTranscript("");
    setSegments([]);
    setIntelligence(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const uploadAndTranscribe = async () => {
    if (!file) {
      setError("Please choose a .wav file to upload.");
      return;
    }

    setLoading(true);
    setError(null);
    setTranscript("");
    setSegments([]);
    setIntelligence(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const resp = await fetch("/api/transcribe_and_analyze", {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`Server error: ${resp.status} ${text}`);
      }

      const data = await resp.json();

      // Expected shape: { text, segments, intelligence }
      setTranscript(data.text ?? "");
      setSegments(Array.isArray(data.segments) ? data.segments : []);
      setIntelligence(data.intelligence ?? null);
    } catch (err) {
      console.error(err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const downloadTranscript = () => {
    const blob = new Blob([transcript || ""], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download =
      file ? `${file.name.replace(/\.[^/.]+$/, "")}_transcript.txt` : "transcript.txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">Smart Meeting Assistant (MVP)</h1>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choose audio (.wav)
          </label>
          <input
            ref={inputRef}
            type="file"
            accept="audio/wav, audio/x-wav, audio/mpeg, audio/*"
            onChange={handleFileChange}
            className="block w-full"
          />
        </div>

        <div className="flex gap-2 mb-6">
          <button
            className={`px-4 py-2 rounded ${
              loading ? "bg-gray-300 cursor-not-allowed" : "bg-blue-600 text-white"
            }`}
            onClick={uploadAndTranscribe}
            disabled={loading}
          >
            {loading ? "Transcribing..." : "Upload & Transcribe"}
          </button>

          <button
            className="px-4 py-2 rounded bg-gray-200"
            onClick={reset}
            disabled={loading}
          >
            Reset
          </button>

          <button
            className="px-4 py-2 rounded bg-green-600 text-white"
            onClick={downloadTranscript}
            disabled={!transcript}
          >
            Download Transcript
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded">
            Error: {error}
          </div>
        )}

        {transcript && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Transcript</h2>
            <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">
              {transcript}
            </pre>
          </div>
        )}

        {segments && segments.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-medium mb-2">Segments</h3>
            <ul className="list-disc pl-5">
              {segments.map((s, i) => (
                <li key={i} className="mb-1">
                  <strong>
                    [{(s.start ?? 0).toFixed(2)} - {(s.end ?? 0).toFixed(2)}]
                  </strong>{" "}
                  {s.text}
                </li>
              ))}
            </ul>
          </div>
        )}

        {intelligence && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-3">Meeting Intelligence</h2>

            <div className="mb-4">
              <h4 className="font-medium">Summary</h4>
              <p className="mt-1 text-gray-700">
                {intelligence.summary ?? intelligence.raw ?? "(no summary)"}
              </p>
            </div>

            <div className="mb-4">
              <h4 className="font-medium">Key Points</h4>
              <ul className="list-disc pl-5 mt-1">
                {(intelligence.key_points || []).map((kp, idx) => (
                  <li key={idx}>{kp}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-medium">Action Items</h4>
              <ul className="list-disc pl-5 mt-1">
                {(intelligence.action_items || []).map((ai, idx) => (
                  <li key={idx}>
                    <strong>{ai.task ?? "(no task)"}</strong>
                    {ai.owner ? ` — ${ai.owner}` : " — unassigned"}
                    {ai.due ? ` (due: ${ai.due})` : ""}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <footer className="text-sm text-gray-500 mt-6">
          Powered by Whisper & LLM Summarization
        </footer>
      </div>
    </div>
  );
}
