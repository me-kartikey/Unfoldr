import api from "@/api/axios";

export const uploadRepository = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/repositories/upload", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};

export const getRepositories = async () => {
    const response = await api.get("/repositories");
    return response.data;
};

export const getRepository = async (id: string) => {
    const response = await api.get(`/repositories/${id}`);
    return response.data;
};

export const getRepositoryAnalysis = async (id: string) => {
    const response = await api.get(`/repositories/${id}/analysis`);
    return response.data;
};

export const getRepositoryArchitecture = async (id: string) => {
    const response = await api.get(`/repositories/${id}/architecture`);
    return response.data;
};

export const getRepositoryDependencies = async (id: string) => {
    const response = await api.get(`/repositories/${id}/dependencies`);
    return response.data;
};

export const getRepositoryDocumentation = async (id: string) => {
    const response = await api.get(`/repositories/${id}/documentation`);
    return response.data;
};

export const getRepositoryFiles = async (id: string) => {
    const response = await api.get(`/repositories/${id}/files`);
    return response.data;
};

export const getFileContent = async (id: string, path: string) => {
    const response = await api.get(`/repositories/${id}/file`, {
        params: { path },
    });
    return response.data;
};

export const askQuestion = async (id: string, question: string) => {
    const response = await api.post(`/chat/${id}`, { question });
    return response.data;
};