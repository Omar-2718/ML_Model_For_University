import express from 'express';
import morgan from 'morgan';
import predictRoute from './routes/predict';
const app = express();

app.use(express.json());

if ((process.env.NODE_ENV = 'dev')) app.use(morgan('dev'));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(predictRoute);
app.get('/', (req, res) => {
  res.status(200).end('ok');
});
app.get('/*splat', (req, res) => {
  return res.status(404).send('404');
});
export default app;
