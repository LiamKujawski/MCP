/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'standalone', // Temporarily disabled for build issues
  reactStrictMode: true,
  swcMinify: true,
  // Performance optimizations for Lighthouse
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react']
  },
  images: {
    formats: ['image/webp'],
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
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