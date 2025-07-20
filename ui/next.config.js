/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
      // WebSocket connections need to be proxied differently
      // Next.js doesn't support ws:// protocol in rewrites
    ];
  },
};

module.exports = nextConfig; 