import client from './client';

export const submitCode = (data) => client.post('/code/submit', data);
