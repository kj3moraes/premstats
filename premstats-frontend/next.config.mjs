/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL,
  },
};

export default nextConfig;
