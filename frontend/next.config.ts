import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  distDir: '.next',
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // Moved server components external packages to the stable option
  serverExternalPackages: [],
  server: {
    turbopack: {
      root: 'frontend'
    }
  },
  // Production configuration
  trailingSlash: false,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
