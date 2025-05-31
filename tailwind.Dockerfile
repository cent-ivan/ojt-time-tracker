FROM node:20-alpine

WORKDIR /flask-app

# Copy frontend dependencies and install with npm
COPY package*.json ./
RUN npm install

# Copy the rest of the app code
COPY . .

# build Tailwind CSS once (like for production).
CMD [ "npm", "run", "build" ]