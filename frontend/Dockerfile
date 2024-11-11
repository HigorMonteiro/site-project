# Use the official Node.js image as the base image
FROM node:22.3.0

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN pnpm install

# Remove node_modules if it exists
RUN rm -rf node_modules

# Copy the rest of the application code
COPY . .


# Expose the port Vite uses
EXPOSE 5173

# Command to run the application
CMD ["pnpm", "run", "dev"]