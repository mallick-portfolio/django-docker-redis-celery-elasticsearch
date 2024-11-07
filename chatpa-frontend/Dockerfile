# Step 1: Build the Next.js app
FROM node:20-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json/yarn.lock for dependency installation
COPY package*.json .

# Install dependencies
RUN npm install

# Copy the rest of the app source code (including app directory)
COPY . .

EXPOSE 3000

# Start the Next.js app in production mode
CMD ["npm", "run", "dev"]
