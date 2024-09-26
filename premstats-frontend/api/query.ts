interface BackendResponse {
    message: string 
}

export const query_backend = async (query: string): Promise<string> => {
    // Construct the search request body
    const requestBody = {
        message: query
    };

    console.log(requestBody)
    // Send a POST request to the search API
    console.log(process.env.BACKEND_API_URL)
    const api_query_path = process.env.BACKEND_API_URL + "/api/query/ask_stats"
    const response = await fetch(`http://localhost:8000/api/query/ask_stats`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
    });
    
    const jsonResponse: BackendResponse = await response.json();
    console.log(jsonResponse) 
    
    return jsonResponse.message;
}
