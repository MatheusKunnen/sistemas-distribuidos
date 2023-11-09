FROM node:20.6.1
ADD ./client  /client 
WORKDIR /client 
EXPOSE 3000
RUN npm install --silent
ENTRYPOINT ["npm", "start"]
