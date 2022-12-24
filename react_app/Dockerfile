FROM node:14.17.3
ENV REACT_DIRECTORY=react_ui
WORKDIR /${REACT_DIRECTORY}
COPY ./${REACT_DIRECTORY}/ .
RUN npm install
RUN yarn add recharts
RUN apt update -y
RUN apt upgrade -y
RUN apt install vim -y
EXPOSE 3000
CMD ["npm", "start"]