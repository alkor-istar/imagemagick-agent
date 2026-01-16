import { useState } from "react"
import { editImage } from "./api/imagickApi"

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [prompt, setPrompt] = useState("")
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit() {
    if (!file || !prompt) return

    setLoading(true)
    setError(null)
    setResultUrl(null)

    try {
      const blob = await editImage(file, prompt)
      setResultUrl(URL.createObjectURL(blob))
    } catch (e) {
      setError("Failed to process image")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex items-center justify-center">
      <div className="w-full max-w-xl bg-gray-800 p-6 rounded-xl shadow-lg space-y-4">
        <h1 className="text-2xl font-bold">
          ImageMagick LLM Agent
        </h1>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="block w-full text-sm"
        />

        <textarea
          placeholder="Describe the edit (e.g. resize to 512x512)"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 py-2 rounded"
        >
          {loading ? "Processing..." : "Edit Image"}
        </button>

        {error && (
          <div className="text-red-400 text-sm">{error}</div>
        )}

        {resultUrl && (
          <div className="pt-4">
            <h2 className="font-semibold mb-2">Result</h2>
            <a href={resultUrl} download>
              <img
                src={resultUrl}
                alt="Result"
                className="rounded border"
              /></a>
          </div>
        )}
      </div>
    </div>
  )
}
