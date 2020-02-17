import express from 'express';
import helmet from 'helmet';
import mongoose from 'mongoose';
import session from 'express-session';
import connectMongo from 'connect-mongo';
import { ApolloServer } from 'apollo-server-express';

import loggerConfig from './config/loggerConfig';

import typeDefs from './graphql/schemas/schemas';
import resolvers from './graphql/resolvers/resolvers';
import schemaDirectives from './graphql/directives/directives';
import dotenv from 'dotenv';
import path from 'path';
// import Image from '../python/Cap1.JPG';
import {spawn} from 'child_process';

dotenv.config({ path: '../../EnvironmentVariables.env' })
const { NODE_ENV, SESSION_NAME, SESSION_SECRET, SESSION_MAX_AGE, MONGO_DB_URI, PORT } = process.env;

const app = express();

mongoose.set('useCreateIndex', true);

// Set Secure Headers with Helmet
app.use(helmet());
app.use(helmet.permittedCrossDomainPolicies());
app.use(express.static('dist'));
//C:\Users\1025040\Documents\git\CysrtallBall\src\python\Cap1.JPG
//C:\Users\1025040\Documents\git\CysrtallBall\src\python\Cap1.JPG
app.get('/images/mask',(req, res) => {
  res.sendFile( path.join(__dirname,'../python/Cap1.JPG'))
})
// Set User Session
const MongoStore = connectMongo(session);
app.use(
  session({
    store: new MongoStore({ mongooseConnection: mongoose.connection }),
    name: SESSION_NAME,
    secret: SESSION_SECRET,
    resave: true,
    rolling: true,
    saveUninitialized: false,
    cookie: {
      maxAge: parseInt(SESSION_MAX_AGE, 10),
      sameSite: true,
      httpOnly: true,
      secure: !NODE_ENV.trim() === 'development'
    }
  })
);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  schemaDirectives,
  playground:
    NODE_ENV.trim() !== 'development'
      ? false
      : {
        settings: {
          'request.credentials': 'include',
          'schema.polling.enable': false
        }
      },
  context: ({ req, res }) => ({ req, res })
});

// Logging with Morgan
if (NODE_ENV === 'development') {
  loggerConfig(app);
}

server.applyMiddleware({
  app,
  cors: {
    credentials: true,
    origin: 'http://localhost:3000'
  }
});

mongoose.connect(MONGO_DB_URI, { useNewUrlParser: true });
mongoose.connection.once('open', () => {
  const port = PORT || 8080;
  app.listen({ port }, () => {
    console.log(`Server running on port ${port}`);
  });
  app.get('/pythonscripts', (req, res) => {
    const pythonProcess = spawn('python',[path.join(__dirname,'../python/segment.py'),path.join(__dirname,'../python/Cap1.JPG')]);
    pythonProcess.stdout.on('data', (data) => {
      console.log("=================",data, data.toJSON());
    });
    return res.send("running python scriptsssssssss");
  })
});
mongoose.connection.on('error', error => console.error(error));
