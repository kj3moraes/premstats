"use client";
import { Input } from "@/components/ui/input";
import Footer from "@/components/footer";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

import React, { useState } from "react";
import { FaFutbol } from "react-icons/fa";
import { query_backend } from "../api/query";

export default function Home() {
  const [response, setResponse] = useState<string>("");
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    console.log("Querying backend with:", query);
    console.log(process.env.BACKEND_API_URL);
    try {
      const response = await query_backend(query);
      setResponse(response);
    } catch (error) {
      console.error("Error querying backend:", error);
      setResponse("An error occurred while fetching the response.");
    } finally {
      setIsLoading(false);
      setQuery("");
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8 flex items-center justify-center">
      <div className="w-full max-w-6xl flex flex-col md:flex-row md:items-center md:justify-between">
        {/* Left Side */}
        <div className="md:w-1/2 mb-8 md:mb-0 flex flex-col items-center md:items-start space-y-2">
          <div className="flex flex-row space-x-4 justify-center">
            <FaFutbol className="text-5xl text-primary-background" />
            <h1 className="text-5xl font-bold mb-4 text-center md:text-left">
              premstats.xyz
            </h1>
          </div>
          <form onSubmit={handleSubmit} className="w-full max-w-md">
            <Input
              type="text"
              placeholder="Ask about any match or team stats..."
              className="w-full mb-2"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            {/* <Button type="submit" className="w-full">
              Submit
            </Button> */}
            <p className="text-sm text-muted-foreground mt-2 text-center md:text-left">
              You can ask about any Premier League season up to but not
              including the current season.
            </p>
          </form>
          <div>
            <Alert className="w-full max-w-md">
              <AlertTitle className='text-lg font-semibold'>Heads up!</AlertTitle>
              <AlertDescription>
                This site is in beta mode and may not be fully functional. Please 
                report any issues to the developer.
              </AlertDescription>
            </Alert>
          </div>
        </div>

        {/* Right side */}
        <div className="md:w-1/2 p-4 rounded-lg">
          <p>{response}</p>
          {isLoading && <p>Loading...</p>}
        </div>
      </div>
    </div>
  );
}
