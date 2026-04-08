import client from './client';

export const getAssignments = () => client.get('/assignments/');
export const getAssignment = (id) => client.get(`/assignments/${id}`);
export const createAssignment = (data) => client.post('/assignments/', data);
export const updateAssignment = (id, data) => client.put(`/assignments/${id}`, data);
export const deleteAssignment = (id) => client.delete(`/assignments/${id}`);
