/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // FastAPI backend
      },
      {
        source: '/ws/:path*',
        destination: 'ws://localhost:8000/ws/:path*', // WebSocket endpoint
      },
    ];
  },
};

module.exports = nextConfig; 