/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config) => {
    // Custom webpack configurations can be added here
    return config;
  },
};

module.exports = nextConfig;