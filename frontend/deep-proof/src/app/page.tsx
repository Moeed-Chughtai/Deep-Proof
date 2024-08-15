"use client";

import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [predictions, setPredictions] = useState<number[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("video", file);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });
      

      if (!response.ok) {
        throw new Error("Failed to fetch predictions");
      }

      const data = await response.json();
      setPredictions(data.predictions);
    } catch (error) {
      console.log(error);
      setError("An error occurred while uploading the video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold text-center mb-4">Upload and Predict</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex flex-col items-center">
            <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
              Choose a video file
            </label>
            <input
              id="file-upload"
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="mt-2 mb-4 border border-gray-300 rounded-lg p-2 cursor-pointer"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
            disabled={loading}
          >
            {loading ? "Processing..." : "Submit"}
          </button>
        </form>

        {error && <p className="mt-4 text-red-500 text-center">{error}</p>}

        {predictions.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2">Predictions</h2>
            <ul className="list-disc list-inside">
              {predictions.map((prediction, index) => (
                <li key={index} className="text-gray-800">
                  Prediction {index + 1}: {prediction.toFixed(2)}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
