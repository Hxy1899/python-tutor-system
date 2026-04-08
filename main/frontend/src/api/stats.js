import client from './client';

export const getOverallStats = () => client.get('/stats/overall');
export const getStudentStats = (id) => client.get(`/stats/student/${id}`);
