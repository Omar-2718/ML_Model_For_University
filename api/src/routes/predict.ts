import express from 'express';
import { predict } from '../controllers/predict.controller';
const route = express.Router();

route.post('/predict', predict);

export default route;
