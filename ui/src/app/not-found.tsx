import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-4xl font-bold mb-4">404</h2>
        <h3 className="text-2xl mb-4">Page Not Found</h3>
        <p className="mb-4">Could not find the requested resource</p>
        <Link 
          href="/"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-block"
        >
          Return Home
        </Link>
      </div>
    </div>
  )
} 