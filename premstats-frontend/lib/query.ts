interface BackendRequest {
  message: string;
}

interface BackendResponse {
  message: string;
  data: Array<{ [key: string]: any }> | number | string;
}

export const query_backend = async (query: string): Promise<string> => {
  // Construct the search request body
  const requestBody: BackendRequest = {
    message: query,
  };

  console.log(requestBody);

  // Send a POST request to the search API
  console.log(process.env.BACKEND_API_URL);
  const api_query_path = process.env.BACKEND_API_URL + '/api/query/ask_stats';
  const response = await fetch(api_query_path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  const jsonResponse = await response.json();
  console.log("The response is ", jsonResponse);  
  if (!response.ok) {
    throw new Error(jsonResponse['detail']);
  }

  return jsonResponse.message;
};
