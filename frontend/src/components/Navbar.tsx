 import Link from 'next/link';

export function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">🤖</span>
              <span className="ml-2 text-xl font-semibold text-gray-900">
                DevOps Co-Pilot
              </span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-6">
            <Link
              href="/"
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Dashboard
            </Link>
            <Link
              href="/incidents"
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Incidents
            </Link>
            <Link
              href="/analytics"
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Analytics
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
