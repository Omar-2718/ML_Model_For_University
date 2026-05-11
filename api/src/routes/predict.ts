import express from 'express';
import { predict, getFeatures } from '../controllers/predict.controller';
const route = express.Router();

route.post('/predict', predict);
route.get('/predict/features', getFeatures);
export default route;
