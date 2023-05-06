/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    API_URL: process.env.API_URL,
  },
  async rewrites() {
    return [
      {
        source: '/api/func/:path*',
        destination: `${process.env.API_URL}:path*`,
      },
    ]
  },
}

module.exports = nextConfig
