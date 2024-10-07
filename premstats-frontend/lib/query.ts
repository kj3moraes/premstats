interface BackendRequest {
  message: string;
}

export interface SuccessResponse {
  message: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: Array<{ [key: string]: any }>;
}

export interface ErrorResponse {
  detail: string;
}

export type BackendResponse = SuccessResponse | ErrorResponse;

export const query_backend = async (
  query: string
): Promise<BackendResponse> => {
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

  const jsonResponse: BackendResponse = await response.json();
  console.log('The response is ', jsonResponse);
  if (!response.ok) {
    if ('detail' in jsonResponse) {
      throw new Error(jsonResponse.detail);
    } else {
      throw new Error('Unknown error occurred.');
    }
  }

  if ('message' in jsonResponse) {
    return jsonResponse;
  } else {
    throw new Error(jsonResponse.detail);
  }
};
