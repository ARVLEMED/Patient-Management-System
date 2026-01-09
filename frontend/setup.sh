#!/bin/bash

# Create directory structure
mkdir -p src/{components,pages,services,context,types}
mkdir -p public

# Create placeholder files
touch src/pages/PatientDashboard.tsx
touch src/pages/WorkerDashboard.tsx
touch src/pages/AdminDashboard.tsx

echo "Frontend structure created!"
echo "Now copy all the code files from the artifacts."