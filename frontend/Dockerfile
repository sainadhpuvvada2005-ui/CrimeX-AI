# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine

WORKDIR /app

# Create a non-root user
RUN addgroup --system nextjs && adduser --system --group nextjs nextjs
USER nextjs

# Copy the standalone output
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Set the port
ENV PORT 3000

EXPOSE ${PORT}

CMD ["node", "server.js"]
