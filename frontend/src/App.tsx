import { useState } from "react";
import { editImage } from "./api/imagickApi";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [prompt, setPrompt] = useState("");
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (!file || !prompt) return;

    setLoading(true);
    setError(null);
    setResultUrl(null);

    try {
      const blob = await editImage(file, prompt);
      setResultUrl(URL.createObjectURL(blob));
    } catch (e) {
      setError("Failed to process image");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex items-center justify-center flex-col">
      <div className="w-full max-w-xl bg-gray-800 p-6 rounded-xl shadow-lg space-y-4">
        <div className="flex items-center gap-4">
          <img
            src="/wizard.png"
            alt="Wizard"
            className="w-40 h-auto rounded-2xl shadow-xl shadow-black/40"
          />
          <h1 className="text-4xl w-full text-center font-display text-gray-400 [text-shadow:0_2px_8px_rgba(0,0,0,0.5)]">
            ImageMagick
            <br /> LLM Agent
          </h1>
        </div>

        <label className="flex cursor-pointer flex-col gap-2">
          <span className="text-sm  text-gray-400">Choose an image</span>
          <div className="relative group flex items-center rounded bg-gray-700 p-2 cursor-pointer">
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="absolute inset-0 cursor-pointer opacity-0"
            />
            <span className="rounded bg-gray-600 cursor-pointer group-hover:bg-gray-500 px-4 py-2 text-sm text-gray-200 transition-colors">
              {file ? file.name : "Browse..."}
            </span>
          </div>
        </label>

        <textarea
          placeholder="Describe the edit (e.g. resize to 512x512)"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-blue-900 hover:bg-amber-600 disabled:opacity-50 py-2 rounded transition-colors"
        >
          {loading ? "Processing..." : "Edit Image"}
        </button>

        {error && <div className="text-red-400 text-sm">{error}</div>}

        {resultUrl && (
          <div className="pt-4">
            <h2 className="font-semibold mb-2">Result</h2>
            <a href={resultUrl} download>
              <img src={resultUrl} alt="Result" className="rounded border" />
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
